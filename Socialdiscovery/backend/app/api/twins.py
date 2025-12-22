from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/twins")
def get_thought_twins():
    return {
        "generated_at": datetime.utcnow(),
        "twins": [
            {
                "user": "alice_nyc",
                "overlap_pct": 87,
                "window": "last_60_minutes",
                "shared_intents": ["AI governance", "agent safety"]
            }
        ]
    }
