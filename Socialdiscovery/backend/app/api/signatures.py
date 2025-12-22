from fastapi import APIRouter
from app.services.signing import sign_payload

router = APIRouter()

@router.post("/sign/policy/{policy_id}")
def sign_policy(policy_id: str):
    policy = load_policy(policy_id)
    signed = sign_payload(policy.to_dict())
    persist_signature(policy_id, signed)
    return signed
