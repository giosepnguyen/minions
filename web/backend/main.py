from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models

app = FastAPI()

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

    from sqlalchemy import func

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