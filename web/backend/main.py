from fastapi import FastAPI, Depends, HTTPException
import json
import re
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from database import get_db, engine
import models

app = FastAPI()

# JSON mock files are stored in ./mock_data relative to this main.py.
MOCK_DATA_DIR = Path(__file__).resolve().parent / "mock_data"


def load_mock_json(filename: str) -> dict:
    """Load a mock response from the mock_data directory."""
    file_path = MOCK_DATA_DIR / filename
    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Mock JSON file not found: {filename}",
        ) from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Mock JSON file is invalid: {filename}",
        ) from exc
# =========================================================
# 1. DATA MODELS
# =========================================================
class UserContext(BaseModel):
    userId: str
    age: int
    gender: Optional[str] = None
    primarySymptoms: List[str]
    patientLocation: Optional[dict] = None
class ConversationMessage(BaseModel):
    role: str
    content: str
    timestamp: str
class AIAssessmentInput(BaseModel):
    sessionId: str
    userContext: UserContext
    conversationHistory: List[ConversationMessage]
class Question(BaseModel):
    id: str
    prompt: str
    inputType: str
    options: Optional[List[str]] = None
class EmergencyFacility(BaseModel):
    name: str
    address: str
    phone: str
    distanceKm: float
class AssessmentResult(BaseModel):
    triageLevel: Optional[str] = None
    possibleConditions: Optional[List[str]] = None
    explanation: Optional[str] = None
    supportingFactors: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None
    warningSigns: Optional[List[str]] = None
    emergencyFacilities: Optional[List[EmergencyFacility]] = None
class NextAction(BaseModel):
    type: str
    question: Optional[Question] = None
    assessmentResult: Optional[AssessmentResult] = None
class AIAssessmentOutput(BaseModel):
    sessionId: str
    status: str
    confidenceScore: float
    nextAction: NextAction
# =========================================================
# 2. QUESTION DEFINITIONS
# =========================================================
DURATION_QUESTION = {
    "id": "q_duration",
    "prompt": "Bạn đã có các triệu chứng này bao lâu rồi?",
    "inputType": "SINGLE_CHOICE",
    "options": [
        "Dưới 24 giờ",
        "1–3 ngày",
        "4–7 ngày",
        "Hơn 1 tuần",
    ],
}
SEVERITY_QUESTION = {
    "id": "q_severity",
    "prompt": "Mức độ triệu chứng của bạn như thế nào?",
    "inputType": "SINGLE_CHOICE",
    "options": [
        "Nhẹ",
        "Vừa",
        "Nặng",
    ],
}
PROGRESSION_QUESTION = {
    "id": "q_progression",
    "prompt": "Triệu chứng của bạn đang nặng hơn, giữ nguyên hay đỡ hơn?",
    "inputType": "SINGLE_CHOICE",
    "options": [
        "Nặng hơn",
        "Giữ nguyên",
        "Đỡ hơn",
    ],
}
ASSOCIATED_SYMPTOMS_QUESTION = {
    "id": "q_associated_symptoms",
    "prompt": "Bạn có sốt, mệt, buồn nôn không?",
    "inputType": "SINGLE_CHOICE",
    "options": [
        "Có sốt",
        "Có mệt",
        "Có buồn nôn",
        "Có nhiều triệu chứng trên",
        "Không có triệu chứng nào trên",
    ],
}
ASSESSMENT_QUESTIONS = [
    DURATION_QUESTION,
    SEVERITY_QUESTION,
    PROGRESSION_QUESTION,
    ASSOCIATED_SYMPTOMS_QUESTION,
]
# =========================================================
# 3. RESPONSE HELPERS
# =========================================================
def question_response(
    session_id: str,
    question: dict,
    confidence: float,
) -> dict:
    return {
        "sessionId": session_id,
        "status": "NEEDS_CLARIFICATION",
        "confidenceScore": confidence,
        "nextAction": {
            "type": "QUESTION",
            "question": question,
            "assessmentResult": None,
        },
    }

def completed_response(
    session_id: str,
    answers: dict,
) -> dict:
    # Use the provided follow-up JSON as the source of the mock result.
    mock = load_mock_json("mock_followup.json")

    supporting_factors = list(mock.get("supporting_factors", []))
    supporting_factors.extend([
        f"Thời gian triệu chứng: {answers['q_duration']}",
        f"Mức độ triệu chứng: {answers['q_severity']}",
        f"Diễn biến triệu chứng: {answers['q_progression']}",
        f"Triệu chứng kèm theo: {answers['q_associated_symptoms']}",
    ])

    return {
        "sessionId": session_id,
        "status": "COMPLETED",
        "confidenceScore": 0.60,
        "nextAction": {
            "type": "RESULT",
            "question": None,
            "assessmentResult": {
                "triageLevel": "MEDIUM",
                "possibleConditions": [],
                "explanation": mock.get("explanation"),
                "supportingFactors": supporting_factors,
                "recommendations": [mock["recommended_action"]]
                    if mock.get("recommended_action") else [],
                "warningSigns": mock.get("warning_signs", []),
                "emergencyFacilities": [],
            },
        },
    }


def emergency_response(session_id: str) -> dict:
    # Use the provided emergency JSON as the source of the mock result.
    mock = load_mock_json("mock_emergency.json")

    facilities = []
    for facility in mock.get("emergency_facilities", []):
        distance_text = str(facility.get("distance", ""))
        distance_match = re.search(r"([0-9]+(?:\\.[0-9]+)?)", distance_text)
        facilities.append({
            "name": facility.get("name", ""),
            "address": facility.get("address", ""),
            "phone": facility.get("phone", ""),
            "distanceKm": float(distance_match.group(1))
                if distance_match else 0.0,
        })

    return {
        "sessionId": session_id,
        "status": "EMERGENCY_REDIRECTIONS",
        "confidenceScore": 1.0,
        "nextAction": {
            "type": "REDIRECT",
            "question": None,
            "assessmentResult": {
                "triageLevel": "CRITICAL",
                "possibleConditions": [],
                "explanation": mock.get("explanation"),
                "supportingFactors": mock.get("supporting_factors", []),
                "recommendations": [mock["recommended_action"]]
                    if mock.get("recommended_action") else [],
                "warningSigns": mock.get("warning_signs", []),
                "emergencyFacilities": facilities,
            },
        },
    }

# =========================================================
# 4. CONVERSATION HISTORY HELPERS
# =========================================================
def identify_question(prompt: str):
    """
    Nhận diện câu hỏi của Backend dựa trên nội dung
    message role=assistant trong conversationHistory.
    """
    normalized_prompt = prompt.strip().lower()
    for index, question in enumerate(ASSESSMENT_QUESTIONS):
        if question["prompt"].strip().lower() in normalized_prompt:
            return index
    return None
def collect_question_answers(history: list) -> dict:
    """
    Thu thập câu trả lời gắn với từng câu hỏi.
    Mỗi câu trả lời được xác định bằng message user xuất hiện
    sau câu hỏi assistant tương ứng và trước câu hỏi assistant
    tiếp theo.
    """
    answers = {}
    for index, message in enumerate(history):
        if message.role.lower() != "assistant":
            continue
        question_index = identify_question(message.content)
        if question_index is None:
            continue
        question_id = ASSESSMENT_QUESTIONS[question_index]["id"]
        # Tìm câu trả lời user kế tiếp trước khi assistant
        # đưa ra một câu hỏi khác.
        for next_message in history[index + 1:]:
            role = next_message.role.lower()
            if role == "assistant":
                break
            if role == "user" and next_message.content.strip():
                answers[question_id] = next_message.content.strip()
                break
    return answers
# =========================================================
# 5. MOCK AI ASSESSMENT
# =========================================================
@app.post(
    "/mock-ai/assessment",
    response_model=AIAssessmentOutput,
)
def mock_ai_assessment(data: AIAssessmentInput):
    session_id = data.sessionId
    history = data.conversationHistory
    # Test case: AI service unavailable
    if session_id == "TEST_AI_SERVICE_ERROR":
        raise HTTPException(
            status_code=503,
            detail={
                "code": "AI_SERVICE_ERROR",
                "message": "AI service is temporarily unavailable",
            },
        )
    # Test case: unexpected internal error
    if session_id == "TEST_INTERNAL_ERROR":
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
            },
        )
    # -----------------------------------------------------
    # A. Emergency screening
    # -----------------------------------------------------
    emergency_keywords = [
        "severe chest pain",
        "chest pain",
        "difficulty breathing",
        "breathing difficulty",
        "shortness of breath",
        "loss of consciousness",
        "đau ngực dữ dội",
        "đau ngực nghiêm trọng",
        "khó thở nghiêm trọng",
        "khó thở dữ dội",
        "không thở được",
        "mất ý thức",
        "bất tỉnh",
    ]
    user_messages = [
        message.content.strip()
        for message in history
        if message.role.lower() == "user"
        and message.content.strip()
    ]
    user_text = " ".join(user_messages).lower()
    symptoms = [
        symptom.strip().lower()
        for symptom in data.userContext.primarySymptoms
    ]
    has_emergency = any(
        keyword in user_text
        or any(keyword in symptom for symptom in symptoms)
        for keyword in emergency_keywords
    )
    if has_emergency:
        return emergency_response(session_id)
    # -----------------------------------------------------
    # B. Identify the latest assistant question
    # -----------------------------------------------------
    last_assistant_index = None
    for index in range(len(history) - 1, -1, -1):
        if history[index].role.lower() == "assistant":
            last_assistant_index = index
            break
    # No assessment question has been asked yet.
    if last_assistant_index is None:
        return question_response(
            session_id,
            DURATION_QUESTION,
            0.45,
        )
    last_assistant_message = history[last_assistant_index]
    current_question_index = identify_question(
        last_assistant_message.content
    )
    # Unexpected history: do not assume the assessment is complete.
    if current_question_index is None:
        return question_response(
            session_id,
            DURATION_QUESTION,
            0.45,
        )
    # -----------------------------------------------------
    # C. Check whether the current question has an answer
    # -----------------------------------------------------
    answers_after_last_question = [
        message.content.strip()
        for message in history[last_assistant_index + 1:]
        if message.role.lower() == "user"
        and message.content.strip()
    ]
    # The current question has not been answered.
    if not answers_after_last_question:
        return question_response(
            session_id,
            ASSESSMENT_QUESTIONS[current_question_index],
            0.45,
        )
    # Collect answers from the complete conversation history.
    answers = collect_question_answers(history)
    # -----------------------------------------------------
    # D. Ask the next question, if any
    # -----------------------------------------------------
    next_question_index = current_question_index + 1
    if next_question_index < len(ASSESSMENT_QUESTIONS):
        next_question = ASSESSMENT_QUESTIONS[next_question_index]
        return question_response(
            session_id,
            next_question,
            min(0.45 + 0.05 * next_question_index, 0.60),
        )
    # -----------------------------------------------------
    # E. Complete only after all four answers are available
    # -----------------------------------------------------
    required_question_ids = [
        question["id"]
        for question in ASSESSMENT_QUESTIONS
    ]
    if all(question_id in answers for question_id in required_question_ids):
        return completed_response(session_id, answers)
    # History is incomplete. Do not fabricate missing answers.
    for question in ASSESSMENT_QUESTIONS:
        if question["id"] not in answers:
            return question_response(
                session_id,
                question,
                0.45,
            )
    # Defensive fallback.
    return question_response(
        session_id,
        DURATION_QUESTION,
        0.45,
    )
# =========================================================
# 6. HEALTH CHECK ASSESSMENT API
# =========================================================
@app.post(
    "/api/v1/assessment/evaluate",
    response_model=AIAssessmentOutput,
)
def evaluate_assessment(data: AIAssessmentInput):
    return mock_ai_assessment(data)
# =========================================================
# 7. CORS
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://vntgtranthieminh-sys.github.io",
        "http://localhost:300",
        "http://127.0.0.1:300",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =========================================================
# 8. BASIC API
# =========================================================
@app.get("/")
def trang_chu():
    return {"message": "Backend đang chạy!"}
# =========================================================
# 9. DATABASE APIs
# =========================================================
@app.get("/api/diseases")
def lay_danh_sach_benh(db: Session = Depends(get_db)):
    return db.query(models.Diseases).all()
@app.get("/api/db-test")
def test_database():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "ok": True,
            "message": "Database connection works!",
        }
    except Exception as e:
        return {
            "ok": False,
            "error_type": type(e).__name__,
            "message": str(e)[:500],
        }
@app.get("/api/symptoms")
def lay_danh_sach_trieu_chung(
    db: Session = Depends(get_db),
):
    return db.query(models.Symptoms).all()
@app.get("/api/diseases-by-symptoms")
def tim_benh_theo_trieu_chung(
    symptom_ids: str,
    db: Session = Depends(get_db),
):
    ids = [
        int(value)
        for value in symptom_ids.split(",")
        if value.strip().isdigit()
    ]
    if not ids:
        return []
    ket_qua = (
        db.query(
            models.Diseases,
            func.count(
                models.DiseaseSymptoms.disease_id
            ).label("so_khop"),
        )
        .join(
            models.DiseaseSymptoms,
            models.DiseaseSymptoms.disease_id
            == models.Diseases.id,
        )
        .filter(
            models.DiseaseSymptoms.symptom_id.in_(ids)
        )
        .group_by(models.Diseases.id)
        .order_by(
            func.count(
                models.DiseaseSymptoms.disease_id
            ).desc()
        )
        .all()
    )
    danh_sach = []
    for benh, so_khop in ket_qua:
        danh_sach.append({
            "id": benh.id,
            "name": benh.name,
            "description": benh.description,
            "causes": benh.causes,
            "treatment": benh.treatment,
            "match_count": so_khop,
        })
    return danh_sach