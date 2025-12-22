# ---- BOOTSTRAP IMPORT PATH ----
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# --------------------------------

from kafka import KafkaConsumer
from app.core.db import SessionLocal
from app.services.aggregate_job import run_aggregation
import json

consumer = KafkaConsumer(
    "events",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode())
)

for msg in consumer:
    event = msg.value
    if event["type"] == "intent_processed":
        db = SessionLocal()
        run_aggregation(
            db,
            summaries=["example summary"] * 30,
            topic=event["payload"]["intent"]
        )
        db.close()
