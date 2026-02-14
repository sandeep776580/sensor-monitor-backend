from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Sensor

router = APIRouter()

@router.get("/")
def get_sensors():
    db = SessionLocal()
    data = db.query(Sensor).order_by(Sensor.timestamp.desc()).limit(50).all()
    db.close()
    return data
