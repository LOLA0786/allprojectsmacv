from datetime import datetime

HUBS = {}

def create_hub(topic: str):
    hid = topic.lower().replace(" ", "-")
    HUBS.setdefault(hid, {
        "id": hid,
        "topic": topic,
        "created_at": datetime.utcnow().isoformat(),
        "signals": []
    })
    return HUBS[hid]

def add_signal(hub_id: str, signal: dict):
    HUBS[hub_id]["signals"].append(signal)
