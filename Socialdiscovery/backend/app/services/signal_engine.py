from collections import Counter
import uuid, time

MIN_MESSAGES = 20   # privacy threshold
MIN_ROOMS = 3

def extract_signals(
    summaries: list[str],
    topic: str,
    window_start: float,
    window_end: float
):
    if len(summaries) < MIN_MESSAGES:
        return None

    words = []
    for s in summaries:
        words.extend(s.lower().split())

    common = [
        w for w, _ in Counter(words).most_common(5)
        if len(w) > 4
    ]

    return {
        "id": str(uuid.uuid4()),
        "topic": topic,
        "window_start": window_start,
        "window_end": window_end,
        "message_count": len(summaries),
        "unique_rooms": len(set(summaries)),
        "key_phrases": common,
        "sentiment": 0.0,  # stub for now
        "created_at": time.time()
    }
