from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.core.uaal import authorize_pour
from app.services.wallet import consume
from app.models.models import Bottle

router = APIRouter(prefix="/pour")

@router.post("/")
def pour(bottle_id: str, restaurant_id: str, ml: int, db: Session = Depends(get_db)):
    bottle = db.query(Bottle).filter(Bottle.id == bottle_id).first()
    if not bottle:
        raise HTTPException(404, "Bottle not found")

    decision = authorize_pour({
        "ml": ml,
        "max_ml": 90
    })

    if decision["decision"] != "ALLOW":
        raise HTTPException(403, decision)

    tx = consume(db, bottle, ml, restaurant_id)
    return {"status": "ok", "tx_id": tx.id}
