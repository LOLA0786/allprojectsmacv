from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode()
)

def emit(event_type: str, payload: dict):
    producer.send(
        "events",
        {
            "type": event_type,
            "payload": payload
        }
    )
