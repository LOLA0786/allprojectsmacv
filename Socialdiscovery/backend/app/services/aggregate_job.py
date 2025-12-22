import time
from app.services.signal_engine import extract_signals
from app.services.insight_repo import save_insight

# UAAL HOOK (FUTURE):
# from uaal import record_decision

def run_aggregation(db, summaries: list[str], topic: str):
    now = time.time()
    window_start = now - 900

    insight = extract_signals(
        summaries=summaries,
        topic=topic,
        window_start=window_start,
        window_end=now
    )

    if not insight:
        return None

    # UAAL.record_decision(...)  ← async, later

    save_insight(db, insight)
    return insight

from app.services.uaal_adapter import record_event
