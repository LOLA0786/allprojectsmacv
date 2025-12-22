from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/mindmap")
def global_mind_map():
    return {
        "timestamp": datetime.utcnow(),
        "bubbles": [
            {"topic": "AI governance", "velocity": "surging", "strength": 0.91},
            {"topic": "job displacement", "velocity": "steady", "strength": 0.62},
            {"topic": "open-source AI", "velocity": "rising", "strength": 0.74}
        ]
    }
