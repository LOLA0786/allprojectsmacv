from fastapi import APIRouter, HTTPException
import uuid
from datetime import datetime

router = APIRouter()

# simple in-memory store (Phase-3C)
_APPEALS = {}

@router.post("/veto/{veto_id}/appeal")
def submit_appeal(veto_id: str, payload: dict):
    if not veto_id:
        raise HTTPException(status_code=400, detail="missing veto_id")

    appeal_id = str(uuid.uuid4())

    appeal = {
        "id": appeal_id,
        "veto_id": veto_id,
        "argument": payload.get("argument"),
        "requested_outcome": payload.get("requested_outcome"),
        "author": payload.get("author"),
        "created_at": datetime.utcnow().isoformat(),
        "status": "pending"
    }

    _APPEALS[appeal_id] = appeal
    return appeal
