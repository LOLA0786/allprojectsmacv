from app.models.models import Bottle, PourTransaction

def create_bottle(db, user_id, brand, ml):
    bottle = Bottle(
        user_id=user_id,
        brand=brand,
        total_ml=ml,
        remaining_ml=ml
    )
    db.add(bottle)
    db.commit()
    return bottle

def consume(db, bottle, ml, restaurant_id):
    if bottle.remaining_ml < ml:
        raise Exception("Insufficient balance")

    bottle.remaining_ml -= ml
    tx = PourTransaction(
        bottle_id=bottle.id,
        restaurant_id=restaurant_id,
        poured_ml=ml
    )
    db.add(tx)
    db.commit()
    return tx
