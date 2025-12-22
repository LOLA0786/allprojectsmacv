from app.services.signal_engine import extract_signals
import time

def test_no_insight_below_threshold():
    summaries = ["short"] * 5
    result = extract_signals(
        summaries,
        topic="laptops",
        window_start=time.time()-100,
        window_end=time.time()
    )
    assert result is None

def test_insight_generated():
    summaries = ["battery life concern"] * 25
    result = extract_signals(
        summaries,
        topic="laptops",
        window_start=time.time()-100,
        window_end=time.time()
    )
    assert result is not None
    assert "battery" in result["key_phrases"]

