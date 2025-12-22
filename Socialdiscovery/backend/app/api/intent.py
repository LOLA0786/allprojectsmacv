from fastapi import APIRouter
import uuid
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/intent")
def get_intent():
    return {
        "id": str(uuid.uuid4()),
        "hub": "ai-governance",
        "topic": "AI governance",
        "momentum": "rising",
        "confidence": 0.87,
        "authenticity": {
            "human_source_pct": 85,
            "ai_assist_pct": 15,
            "label": "Human-Sourced Momentum"
        },
        "ethics": {
            "human_input": 0.7,
            "ai_input": 0.3,
            "moderated": True
        },
        "expires_at": (datetime.utcnow() + timedelta(hours=24)).isoformat()
    }
