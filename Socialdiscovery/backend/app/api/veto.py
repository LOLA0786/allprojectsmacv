from fastapi import APIRouter
from app.services.policy_engine import evaluate_veto

router = APIRouter()

@router.patch("/cocreation/{id}/veto")
def apply_veto(id: str):
    cocreation = load_cocreation(id)
    policy = load_active_policy(scope=f"hub:{cocreation['hub']}")

    decision = evaluate_veto(policy, cocreation)
    persist(decision)

    return {
        "outcome": decision.outcome,
        "reason": decision.reason,
        "policy_id": policy.id
    }
