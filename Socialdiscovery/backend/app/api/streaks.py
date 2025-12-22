from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/streaks")
def intent_streaks():
    return {
        "user": "current_user",
        "active_streaks": [
            {
                "intent": "AI governance",
                "days": 7,
                "countries_connected": 12,
                "people": 23
            }
        ],
        "checked_at": datetime.utcnow()
    }
