from fastapi import FastAPI
from app.database import Base, engine
from app.mqtt_client import start_mqtt
from app.routes import sensor, alerts

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(sensor.router, prefix="/sensors")
app.include_router(alerts.router, prefix="/alerts")

@app.on_event("startup")
def startup_event():
    start_mqtt()
