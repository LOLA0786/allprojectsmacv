from app.services.match_engine import match_intent

def test_match_create_when_empty():
    result = match_intent([1, 0, 0], [])
    assert result["action"] == "create"

def test_match_join_when_similar():
    active = [{
        "moment_id": "m1",
        "embedding": [1, 0, 0]
    }]

    result = match_intent([0.99, 0.01, 0], active)
    assert result["action"] == "join"
    assert result["moment_id"] == "m1"

