from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from datetime import datetime
import time
import hashlib

from app.db.deps import get_db
from app.core.auth_guard import require_role
from app.models.models import Bottle, Transaction

router = APIRouter(prefix="/pos", tags=["pos"])

QR_TTL_SECONDS = 30


@router.post("/authorize-pour")
def authorize_pour(
    payload: dict,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    db: Session = Depends(get_db),
    restaurant = Depends(require_role("RESTAURANT"))
):
    bottle_id = payload.get("bottle_id")
    pour_ml = payload.get("pour_ml")
    qr_issued_at = payload.get("qr_issued_at")

    if not bottle_id or not pour_ml or not qr_issued_at:
        raise HTTPException(400, "Missing fields")

    # 1️⃣ Idempotency (double scan protection)
    existing = (
        db.query(Transaction)
        .filter(Transaction.scan_id == idempotency_key)
        .first()
    )
    if existing:
        return {
            "decision": existing.decision,
            "remaining_ml": existing.remaining_ml,
            "tx_id": existing.id,
            "evidence_id": existing.evidence_id
        }

    # 2️⃣ QR expiry (replay protection)
    if time.time() - qr_issued_at > QR_TTL_SECONDS:
        raise HTTPException(403, "QR_EXPIRED")

    # 3️⃣ Lock bottle row (race protection)
    bottle = (
        db.query(Bottle)
        .filter(Bottle.id == bottle_id)
        .with_for_update()
        .first()
    )

    if not bottle:
        raise HTTPException(404, "Bottle not found")

    if bottle.remaining_ml < pour_ml:
        raise HTTPException(403, "INSUFFICIENT_BALANCE")

    # 4️⃣ Apply pour
    bottle.remaining_ml -= pour_ml

    # 5️⃣ Evidence hash (audit-grade)
    evidence_raw = f"{bottle.id}{pour_ml}{restaurant['sub']}{idempotency_key}"
    evidence_id = hashlib.sha256(evidence_raw.encode()).hexdigest()

    tx = Transaction(
        scan_id=idempotency_key,
        bottle_id=bottle.id,
        restaurant_id=restaurant["sub"],
        pour_ml=pour_ml,
        decision="ALLOW",
        remaining_ml=bottle.remaining_ml,
        evidence_id=evidence_id,
        created_at=datetime.utcnow()
    )

    db.add(tx)
    db.commit()

    return {
        "decision": "ALLOW",
        "remaining_ml": bottle.remaining_ml,
        "tx_id": tx.id,
        "evidence_id": evidence_id
    }
