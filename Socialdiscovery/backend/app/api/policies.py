from fastapi import APIRouter
import uuid
from app.models.policy import Policy

router = APIRouter()

@router.post("/policies")
def create_policy(payload: dict):
    return Policy(
        id=str(uuid.uuid4()),
        scope=payload["scope"],
        rules=payload["rules"],
        authored_by=payload.get("authored_by", []),
        signed=False
    )
