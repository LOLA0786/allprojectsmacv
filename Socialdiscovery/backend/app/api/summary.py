from fastapi import APIRouter, Depends
from app.core.db import get_db
from app.models.moment import Moment

router = APIRouter(prefix="/summary")

@router.get("")
def get_summary(db=Depends(get_db)):
    moment = (
        db.query(Moment)
        .order_by(Moment.created_at.desc())
        .first()
    )

    if not moment or not moment.summary:
        return {"summary": "No active discussion yet."}

    return {"summary": moment.summary}
