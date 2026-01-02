from sqlalchemy import func
from app.models.models import PourTransaction

def yearly_consumption(db, user_id, year):
    return db.query(
        func.sum(PourTransaction.poured_ml).label("total_ml"),
        func.count(PourTransaction.id).label("sessions")
    ).join(
        Bottle, Bottle.id == PourTransaction.bottle_id
    ).filter(
        Bottle.user_id == user_id
    ).all()
