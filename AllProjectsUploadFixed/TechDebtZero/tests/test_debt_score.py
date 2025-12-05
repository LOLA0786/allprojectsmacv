from src.metrics.debt_score import compute_debt_score

def test_score_range():
    score = compute_debt_score()
    assert 0 <= score <= 100
