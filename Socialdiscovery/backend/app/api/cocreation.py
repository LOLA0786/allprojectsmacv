from fastapi import APIRouter
import uuid

router = APIRouter()

# Minimal in-memory store (already matches your existing behavior)
_COCREATIONS = {}

@router.post("/cocreation/{intent_id}")
def create_cocreation(intent_id: str):
    cid = str(uuid.uuid4())
    cocreation = {
        "id": cid,
        "intent_id": intent_id,
        "provenance": {"human": 0.4, "ai": 0.6},
        "status": "draft"
    }
    _COCREATIONS[cid] = cocreation
    return cocreation

@router.patch("/cocreation/{cocreation_id}/veto")
def veto_cocreation(cocreation_id: str):
    cocreation = _COCREATIONS.get(cocreation_id)
    if not cocreation:
        return {"error": "not found"}

    cocreation["vetoed"] = True
    return {
        "veto_id": str(uuid.uuid4()),
        "cocreation_id": cocreation_id
    }
