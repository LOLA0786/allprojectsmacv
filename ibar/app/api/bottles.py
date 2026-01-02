from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.core.auth_guard import require_role
from app.models.models import Bottle

router = APIRouter(prefix="/bottles", tags=["bottles"])


@router.post("/create")
def create_bottle(
    payload: dict,
    db: Session = Depends(get_db),
    account = Depends(require_role("USER"))
):
    brand = payload.get("brand")
    total_ml = payload.get("total_ml")

    if not brand or not total_ml:
        raise HTTPException(400, "brand and total_ml required")

    bottle = Bottle(
        user_id=account["sub"],
        brand=brand,
        total_ml=total_ml,
        remaining_ml=total_ml
    )

    db.add(bottle)
    db.commit()
    db.refresh(bottle)

    return {
        "bottle_id": bottle.id,
        "brand": bottle.brand,
        "remaining_ml": bottle.remaining_ml
    }
