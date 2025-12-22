from app.core.redis import redis_client

def join(room_id: str):
    redis_client.incr(f"room:{room_id}:users")

def leave(room_id: str):
    redis_client.decr(f"room:{room_id}:users")

def users(room_id: str) -> int:
    return int(redis_client.get(f"room:{room_id}:users") or 0)

import time

typing_activity = {}

def register_typing(room_id: str):
    now = time.time()
    typing_activity.setdefault(room_id, [])
    typing_activity[room_id].append(now)

    # keep only last 10 seconds
    typing_activity[room_id] = [
        t for t in typing_activity[room_id] if now - t < 10
    ]

def typing_velocity(room_id: str) -> int:
    now = time.time()
    if room_id not in typing_activity:
        return 0
    return len([t for t in typing_activity[room_id] if now - t < 10])
