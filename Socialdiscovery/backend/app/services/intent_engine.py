import time
import uuid
from typing import Dict

MAX_LEN = 200

def normalize(text: str) -> str:
    return text.strip().lower()[:MAX_LEN]

def urgency_score(confidence: float) -> float:
    return min(max(confidence, 0.0), 1.0)

def build_intent(raw: str, confidence: float) -> Dict:
    now = time.time()
    return {
        "intent_id": str(uuid.uuid4()),
        "semantic_core": normalize(raw),
        "urgency": urgency_score(confidence),
        "created_at": now,
        "expires_at": now + 600
    }
