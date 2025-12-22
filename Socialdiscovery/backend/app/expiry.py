from datetime import datetime

INTENT_STORE = {}

def add_intent(intent: dict):
    INTENT_STORE[intent["id"]] = intent

def purge_expired():
    now = datetime.utcnow()
    expired = [
        k for k, v in INTENT_STORE.items()
        if datetime.fromisoformat(v["expires_at"]) < now
    ]
    for k in expired:
        del INTENT_STORE[k]
