from app.models.models import Bottle

def create_bottle(db, user_id, brand, total_ml):
    bottle = Bottle(
        user_id=user_id,
        brand=brand,
        total_ml=total_ml,
        remaining_ml=total_ml
    )
    db.add(bottle)
    db.commit()
    db.refresh(bottle)
    return bottle
