
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, text

from database import get_db, engine
import models


app = FastAPI()


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
# 2. HELPER FUNCTIONS
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
    "options": ["Nhẹ", "Vừa", "Nặng"],
}


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
        },
    }


def completed_response(
    session_id: str,
    duration: str,
    severity: str,
) -> dict:
    return {
        "sessionId": session_id,
        "status": "COMPLETED",
        "confidenceScore": 0.60,
        "nextAction": {
            "type": "RESULT",
            "assessmentResult": {
                "triageLevel": "MEDIUM",
                "possibleConditions": [],
                "explanation": (
                    "Đây là kết quả mô phỏng để kiểm thử giao diện. "
                    "Chưa đủ thông tin để xác định nguyên nhân "
                    "triệu chứng hoặc đưa ra chẩn đoán."
                ),
                "supportingFactors": [
                    f"Thời gian triệu chứng: {duration}",
                    f"Mức độ triệu chứng: {severity}",
                ],
                "recommendations": [
                    "Theo dõi diễn biến triệu chứng.",
                    "Trao đổi với nhân viên y tế nếu triệu chứng "
                    "kéo dài hoặc nặng lên.",
                ],
                "warningSigns": [
                    "Khó thở",
                    "Đau ngực dữ dội",
                    "Ngất hoặc mất ý thức",
                ],
            },
        },
    }


def emergency_response(session_id: str) -> dict:
    return {
        "sessionId": session_id,
        "status": "EMERGENCY_REDIRECTIONS",
        "confidenceScore": 1.0,
        "nextAction": {
            "type": "REDIRECT",
            "assessmentResult": {
                "triageLevel": "CRITICAL",
                "explanation": (
                    "Thông tin được cung cấp có thể cho thấy "
                    "tình trạng cấp cứu cần được đánh giá ngay."
                ),
                "recommendations": [
                    "Gọi cấp cứu 115 tại Việt Nam nếu đang có "
                    "triệu chứng nguy hiểm.",
                    "Không tự lái xe nếu tình trạng sức khỏe "
                    "không ổn định.",
                    "Nhờ người ở gần hỗ trợ trong khi chờ "
                    "nhân viên cấp cứu.",
                ],
                "warningSigns": [
                    "Đau ngực dữ dội",
                    "Khó thở nghiêm trọng",
                    "Mất ý thức",
                ],
            },
        },
    }


# =========================================================
# 3. MOCK AI ASSESSMENT
# =========================================================

@app.post(
    "/mock-ai/assessment",
    response_model=AIAssessmentOutput,
)
def mock_ai_assessment(data: AIAssessmentInput):

    session_id = data.sessionId

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
    # Check user-provided information, not assistant prompts.
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
        for message in data.conversationHistory
        if message.role.lower() == "user"
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
    # B. Determine which question was answered most recently
    # -----------------------------------------------------

    history = data.conversationHistory

    last_assistant_index = None

    for index in range(len(history) - 1, -1, -1):
        if history[index].role.lower() == "assistant":
            last_assistant_index = index
            break

    last_assistant_prompt = ""

    if last_assistant_index is not None:
        last_assistant_prompt = (
            history[last_assistant_index].content.strip().lower()
        )

    # Find user answers after the most recent assistant message.
    # This avoids relying on the total number of old answers.
    answers_after_last_question = []

    if last_assistant_index is not None:
        answers_after_last_question = [
            message.content.strip()
            for message in history[last_assistant_index + 1:]
            if message.role.lower() == "user"
            and message.content.strip()
        ]

    # If the most recent assistant message was the duration
    # question and the user answered it, ask about severity.
    duration_prompt = DURATION_QUESTION["prompt"].lower()
    severity_prompt = SEVERITY_QUESTION["prompt"].lower()

    answered_duration = (
        duration_prompt in last_assistant_prompt
        and len(answers_after_last_question) > 0
    )

    answered_severity = (
        severity_prompt in last_assistant_prompt
        and len(answers_after_last_question) > 0
    )

    # Case 1: No duration answer has been given yet.
    if not user_messages or (
        last_assistant_index is not None
        and duration_prompt in last_assistant_prompt
        and not answers_after_last_question
    ):
        return question_response(
            session_id,
            DURATION_QUESTION,
            0.45,
        )

    # Case 2: Duration was answered; ask about severity.
    if answered_duration:
        return question_response(
            session_id,
            SEVERITY_QUESTION,
            0.55,
        )

    # Case 3: Severity was answered; complete the mock assessment.
    if answered_severity:
        duration_answer = next(
            (
                message.content.strip()
                for message in reversed(history[:last_assistant_index])
                if message.role.lower() == "user"
                and message.content.strip()
            ),
            "Chưa cung cấp",
        )

        severity_answer = answers_after_last_question[-1]

        return completed_response(
            session_id,
            duration_answer,
            severity_answer,
        )

    # Fallback for an unexpected conversation state.
    # Do not invent a medical conclusion.
    return question_response(
        session_id,
        DURATION_QUESTION,
        0.45,
    )


# =========================================================
# 4. HEALTH CHECK ASSESSMENT API
# =========================================================

@app.post(
    "/api/v1/assessment/evaluate",
    response_model=AIAssessmentOutput,
)
def evaluate_assessment(data: AIAssessmentInput):
    return mock_ai_assessment(data)


# =========================================================
# 5. CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# 6. BASIC API
# =========================================================

@app.get("/")
def trang_chu():
    return {"message": "Backend đang chạy!"}


# =========================================================
# 7. DATABASE APIs
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
