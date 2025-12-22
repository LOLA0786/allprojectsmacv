from app.services.intent_engine import build_intent

def test_build_intent_basic():
    intent = build_intent("Choosing MacBook Air", 0.9)

    assert intent["semantic_core"] == "choosing macbook air"
    assert 0 <= intent["urgency"] <= 1
    assert intent["expires_at"] > intent["created_at"]

def test_intent_truncation():
    long_text = "x" * 500
    intent = build_intent(long_text, 1.2)

    assert len(intent["semantic_core"]) <= 200
    assert intent["urgency"] == 1.0

