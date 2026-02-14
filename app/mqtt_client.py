import json
import paho.mqtt.client as mqtt
from app.config import MQTT_BROKER, MQTT_PORT, MQTT_TOPICS
from app.database import SessionLocal
from app.models import Sensor, Alert
from app.thresholds import THRESHOLDS

def on_message(client, userdata, msg):
    db = SessionLocal()
    payload = json.loads(msg.payload.decode())

    sensor = Sensor(
        topic=msg.topic,
        temperature=payload["temperature"],
        humidity=payload["humidity"],
        voltage=payload["voltage"],
        current=payload["current"],
        pressure=payload["pressure"]
    )
    db.add(sensor)

    violated = [k for k,v in payload.items() if k in THRESHOLDS and v > THRESHOLDS[k]]

    if violated:
        alert = Alert(
            topic=msg.topic,
            violated_params=",".join(violated),
            values=json.dumps(payload)
        )
        db.add(alert)

    db.commit()
    db.close()

def start_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT)

    for topic in MQTT_TOPICS:
        client.subscribe(topic)

    client.loop_start()
