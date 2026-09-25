from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models
from sqlalchemy import text
from database import get_db, engine

app = FastAPI()
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

@app.post(
    "/api/v1/assessment/evaluate",
    response_model=AIAssessmentOutput
)
def evaluate_assessment(data: AIAssessmentInput):
    symptoms = [s.lower() for s in data.userContext.primarySymptoms]

    conversation_text = " ".join(
        message.content.lower()
        for message in data.conversationHistory
    )

    # MOCK 3: Emergency Redirection
    emergency_keywords = [
        "severe chest pain",
        "chest pain",
        "difficulty breathing",
        "breathing difficulty",
        "shortness of breath",
        "loss of consciousness",
    ]

    has_emergency = any(
        keyword in symptoms or keyword in conversation_text
        for keyword in emergency_keywords
    )

    if has_emergency:
        return {
            "sessionId": data.sessionId,
            "status": "EMERGENCY_REDIRECTIONS",
            "confidenceScore": 1.0,
            "nextAction": {
                "type": "REDIRECT",
                "assessmentResult": {
                    "triageLevel": "CRITICAL",
                    "explanation": (
                        "CRITICAL: Severe chest pain and sudden breathing "
                        "difficulty require immediate emergency medical care."
                    ),
                    "recommendations": [
                        "Call emergency services (115) immediately.",
                        "Do not drive yourself; seek immediate assistance."
                    ],
                    "warningSigns": [
                        "Severe chest pain",
                        "Sudden breathing difficulty"
                    ],
                    "emergencyFacilities": [
                        {
                            "name": "Viet Tiep Friendship Hospital (Emergency Dept)",
                            "address": "1 Nha Thuong St, Le Chan, Hai Phong",
                            "phone": "0225 6292 115",
                            "distanceKm": 1.2
                        }
                    ]
                }
            }
        }

    # MOCK 2: Assessment Completed
    completed_keywords = [
        "2 days",
        "2 day",
        "2 days ago",
        "2 ngày",
        "2 hôm"
    ]

    has_completed_data = (
        any("fever" in symptom for symptom in symptoms)
        and any("headache" in symptom for symptom in symptoms)
        and any(keyword in conversation_text for keyword in completed_keywords)
    )

    if has_completed_data:
        return {
            "sessionId": data.sessionId,
            "status": "COMPLETED",
            "confidenceScore": 0.88,
            "nextAction": {
                "type": "RESULT",
                "assessmentResult": {
                    "triageLevel": "MEDIUM",
                    "possibleConditions": [
                        "Acute Viral Respiratory Infection"
                    ],
                    "explanation": (
                        "Your symptoms of fever, headache, and fatigue "
                        "over 2 days are consistent with a common viral infection."
                    ),
                    "supportingFactors": [
                        "Fever for 2 days",
                        "Headache and fatigue"
                    ],
                    "recommendations": [
                        "Rest and maintain high fluid intake.",
                        "Monitor body temperature twice daily.",
                        "Consult a healthcare professional if symptoms worsen."
                    ],
                    "warningSigns": [
                        "Shortness of breath",
                        "High fever above 39°C persisting for 3 days"
                    ]
                }
            }
        }

    # MOCK 1: Needs Clarification
    return {
        "sessionId": data.sessionId,
        "status": "NEEDS_CLARIFICATION",
        "confidenceScore": 0.45,
        "nextAction": {
            "type": "QUESTION",
            "question": {
                "id": "q_duration",
                "prompt": "How long have you been experiencing these symptoms?",
                "inputType": "SINGLE_CHOICE",
                "options": [
                    "Less than 24 hours",
                    "1-3 days",
                    "4-7 days",
                    "More than 1 week"
                ]
            }
        }
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def trang_chu():
    return {"message": "Backend đang chạy!"}

@app.get("/api/diseases")
def lay_danh_sach_benh(db: Session = Depends(get_db)):
    ds_benh = db.query(models.Diseases).all()
    return ds_benh

@app.get("/api/db-test")
def test_database():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "ok": True,
            "message": "Database connection works!"
        }

    except Exception as e:
        return {
            "ok": False,
            "error_type": type(e).__name__,
            "message": str(e)[:500]
        }

@app.get("/api/symptoms")
def lay_danh_sach_trieu_chung(db: Session = Depends(get_db)):
    return db.query(models.Symptoms).all()

@app.get("/api/diseases-by-symptoms")
def tim_benh_theo_trieu_chung(symptom_ids: str, db: Session = Depends(get_db)):
    ids = [int(x) for x in symptom_ids.split(",") if x.strip().isdigit()]
    if not ids:
        return []

    ket_qua = (
        db.query(models.Diseases, func.count(models.DiseaseSymptoms.disease_id).label("so_khop"))
        .join(models.DiseaseSymptoms, models.DiseaseSymptoms.disease_id == models.Diseases.id)
        .filter(models.DiseaseSymptoms.symptom_id.in_(ids))
        .group_by(models.Diseases.id)
        .order_by(func.count(models.DiseaseSymptoms.disease_id).desc())
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
