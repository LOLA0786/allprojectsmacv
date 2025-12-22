def emit(event_type: str, payload: dict):
    try:
        from app.core.redis import redis_client
        redis_client.xadd(
            "events",
            {"type": event_type, "payload": str(payload)}
        )
    except Exception as e:
        print("Event emit failed (non-fatal):", e)
