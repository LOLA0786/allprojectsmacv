import time
from sqlalchemy.orm import Session
from app.models.moment import Moment

MOMENT_TTL = 600  # 10 minutes

def create_moment(db: Session, intent: dict, active) -> Moment:
    now = time.time()

    # Normalize active → list
    if not active:
        active = []
    elif not isinstance(active, list):
        active = [active]

    intent_text = intent["semantic_core"]

    if active:
        moment = active[0]
        moment.users += 1
        moment.expires_at = now + MOMENT_TTL
        db.commit()
        db.refresh(moment)
        return moment

    moment = Moment(
        intent=intent_text,
        embedding=[1.0, 0.0, 0.0],
        users=1,
        created_at=now,
        expires_at=now + MOMENT_TTL
    )

    db.add(moment)
    db.commit()
    db.refresh(moment)
    return moment
