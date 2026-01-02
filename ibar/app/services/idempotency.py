from app.models.idempotency import IdempotencyKey

def check_and_store(db, key: str, scope: str):
    exists = db.query(IdempotencyKey).filter_by(key=key).first()
    if exists:
        raise Exception("Duplicate request detected")

    db.add(IdempotencyKey(key=key, scope=scope))
    db.commit()
