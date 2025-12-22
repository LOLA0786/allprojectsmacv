import uuid

SUBS = {}

def subscribe(hub: str):
    sid = f"anon-{uuid.uuid4()}"
    SUBS.setdefault(hub, []).append(sid)
    return {"sub_id": sid, "active": True}

def get_subs(hub: str):
    return SUBS.get(hub, [])
