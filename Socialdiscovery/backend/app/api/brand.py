from fastapi import APIRouter, Depends
from app.core.db import get_db
from app.services.brand_insights import (
    trending_topics,
    trending_words,
    ai_topics,
    trending_ideas,
)

router = APIRouter(prefix="/brand")

@router.get("/insights")
def insights(db=Depends(get_db)):
    return {
        "trending_topics": trending_topics(db),
        "trending_words": trending_words(db),
        "ai_topics": ai_topics(db),
        "ideas": trending_ideas(db),
    }
