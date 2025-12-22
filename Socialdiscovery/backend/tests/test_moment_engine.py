from app.services.moment_engine import new_moment, touch, decay, is_dead
import time

def test_new_moment():
    intent = {
        "semantic_core": "test intent"
    }
    m = new_moment(intent, [0.1, 0.2])

    assert m["users"] == 1
    assert m["expires_at"] > time.time()

def test_touch_extends_life():
    m = {
        "users": 1,
        "expires_at": time.time() + 10
    }
    old_expiry = m["expires_at"]
    touch(m)
    assert m["users"] == 2
    assert m["expires_at"] > old_expiry

def test_decay_and_death():
    m = {
        "users": 1,
        "expires_at": time.time() - 1
    }
    decay(m)
    assert is_dead(m)

