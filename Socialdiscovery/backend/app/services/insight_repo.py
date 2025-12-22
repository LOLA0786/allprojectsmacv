from sqlalchemy.orm import Session
from app.models.insight import Insight

def save_insight(db: Session, data: dict):
    row = Insight(**data)
    db.add(row)
    db.commit()

def get_recent_insights(db: Session, topic: str | None = None):
    q = db.query(Insight)
    if topic:
        q = q.filter(Insight.topic == topic)
    return q.order_by(Insight.created_at.desc()).limit(20).all()
