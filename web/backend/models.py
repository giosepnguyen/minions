from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from database import Base

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

class Diseases(Base):
    __tablename__ = "diseases"
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("category.id"))
    name = Column(String(255))
    description = Column(Text)
    causes = Column(Text)
    treatment = Column(Text)

class Symptoms(Base):
    __tablename__ = "symptoms"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class DiseaseSymptoms(Base):
    __tablename__ = "disease_symptoms"
    disease_id = Column(Integer, ForeignKey("diseases.id"), primary_key=True)
    symptom_id = Column(Integer, ForeignKey("symptoms.id"), primary_key=True)

class Prevention(Base):
    __tablename__ = "prevention"
    id = Column(Integer, primary_key=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"))
    recommendation = Column(Text)

class References(Base):
    __tablename__ = "references"
    id = Column(Integer, primary_key=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"))
    organization = Column(String(255))
    url = Column(String(500))

class EmergencyWarning(Base):
    __tablename__ = "emergency_warning"
    id = Column(Integer, primary_key=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"))
    warning = Column(Text)
    severity = Column(String(50))

class UsageStatistics(Base):
    __tablename__ = "usage_statistics"
    id = Column(Integer, primary_key=True)
    feature = Column(String(255))
    created_at = Column(TIMESTAMP)

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255))
    question = Column(Text)
    answer = Column(Text)
    created_at = Column(TIMESTAMP)