from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.db.deps import get_db
from app.core.auth_guard import require_role
from app.models.models import Transaction, Bottle

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/yearly")
def yearly_wrapped(
    year: int,
    db: Session = Depends(get_db),
    user = Depends(require_role("USER"))
):
    start = datetime(year, 1, 1)
    end = datetime(year + 1, 1, 1)

    total_ml = (
        db.query(func.sum(Transaction.pour_ml))
        .filter(
            Transaction.decision == "ALLOW",
            Transaction.created_at >= start,
            Transaction.created_at < end
        )
        .scalar()
        or 0
    )

    top_brand = (
        db.query(Bottle.brand, func.sum(Transaction.pour_ml).label("ml"))
        .join(Transaction, Transaction.bottle_id == Bottle.id)
        .filter(
            Transaction.decision == "ALLOW",
            Transaction.created_at >= start,
            Transaction.created_at < end
        )
        .group_by(Bottle.brand)
        .order_by(func.sum(Transaction.pour_ml).desc())
        .first()
    )

    return {
        "year": year,
        "total_ml": total_ml,
        "top_brand": top_brand[0] if top_brand else None
    }
