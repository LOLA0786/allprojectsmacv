import hashlib
import json
import time

def record_event(event_type: str, payload: dict):
    """
    Async-safe audit hook.
    Replace body with UAAL SDK later.
    """
    evidence = {
        "event": event_type,
        "hash": hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest(),
        "timestamp": time.time(),
    }

    # UAAL.send(evidence)  ← later
    print("[UAAL]", evidence)
