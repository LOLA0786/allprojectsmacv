from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter()

@router.post("/appeal/{appeal_id}/resolve")
def resolve_appeal(appeal_id: str, payload: dict):
    votes = payload.get("votes", 0)

    if votes < 1:
        raise HTTPException(status_code=400, detail="insufficient votes")

    resolution = {
        "appeal_id": appeal_id,
        "outcome": "revise",
        "votes": votes,
        "resolved_by": "quorum",
        "resolved_at": datetime.utcnow().isoformat()
    }

    return resolution
