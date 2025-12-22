from sqlalchemy.orm import Session
from app.models.moment import Moment
from math import sqrt

SIM_THRESHOLD = 0.8

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = sqrt(sum(x * x for x in a))
    mag_b = sqrt(sum(y * y for y in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

def match_intent(db: Session, embedding: list[float], now: float):
    """
    Returns list of active Moment ORM objects
    """
    moments = (
        db.query(Moment)
        .filter(Moment.expires_at > now)
        .all()
    )

    matches = []
    for m in moments:
        if not m.embedding:
            continue

        score = cosine(embedding, m.embedding)
        if score >= SIM_THRESHOLD:
            matches.append(m)

    return matches
