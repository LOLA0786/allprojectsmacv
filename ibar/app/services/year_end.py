from sqlalchemy import func, extract
from app.models.models import PourTransaction, Bottle
from app.models.consumption_yearly import ConsumptionYearly

def generate_yearly(db, user_id, year):
    rows = db.query(
        func.sum(PourTransaction.poured_ml),
        func.count(PourTransaction.id)
    ).join(
        Bottle, Bottle.id == PourTransaction.bottle_id
    ).filter(
        Bottle.user_id == user_id,
        extract("year", PourTransaction.created_at) == year
    ).first()

    total_ml, sessions = rows or (0, 0)

    summary = ConsumptionYearly(
        user_id=user_id,
        year=year,
        total_ml=total_ml or 0,
        total_sessions=sessions or 0,
        max_single_day_ml=0  # can compute later
    )

    db.merge(summary)
    db.commit()
