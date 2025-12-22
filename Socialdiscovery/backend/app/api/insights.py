from fastapi import APIRouter, Depends, Query
from app.core.db import SessionLocal
from app.services.insight_repo import get_recent_insights

router = APIRouter()

def db():
    s = SessionLocal()
    try:
        yield s
    finally:
        s.close()

@router.get("/")
def insights(topic: str | None = Query(None), db=Depends(db)):
    rows = get_recent_insights(db, topic)

    return [
        {
            "topic": r.topic,
            "window": [r.window_start, r.window_end],
            "volume": r.message_count,
            "rooms": r.unique_rooms,
            "phrases": r.key_phrases,
            "sentiment": r.sentiment
        }
        for r in rows
    ]
