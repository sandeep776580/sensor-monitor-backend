from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Alert

router = APIRouter()

@router.get("/")
def get_alerts():
    db = SessionLocal()
    data = db.query(Alert).order_by(Alert.timestamp.desc()).all()
    db.close()
    return data
