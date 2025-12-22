from sqlalchemy.orm import Session
from app.models.moment import Moment

def save_moment(db: Session, m: dict):
    row = Moment(
        id=m["moment_id"],
        intent=m["intent"],
        embedding=m["embedding"],
        users=m["users"],
        created_at=m["created_at"],
        expires_at=m["expires_at"]
    )
    db.merge(row)
    db.commit()

def load_active_moments(db: Session, now: float):
    rows = db.query(Moment).filter(Moment.expires_at > now).all()
    return [
        {
            "moment_id": r.id,
            "intent": r.intent,
            "embedding": r.embedding,
            "users": r.users,
            "created_at": r.created_at,
            "expires_at": r.expires_at
        }
        for r in rows
    ]

