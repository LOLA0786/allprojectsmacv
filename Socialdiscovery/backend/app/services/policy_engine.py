import uuid
from app.models.veto import VetoDecision
from app.models.policy_evidence import PolicyEvidence
from app.uaal import authorize_and_record

def evaluate_veto(policy, cocreation):
    rules = policy.rules
    evidence = {
        "human_pct": cocreation["provenance"]["human"],
        "ai_pct": cocreation["provenance"]["ai"],
        "rules": rules
    }

    if rules.get("min_human_pct") and cocreation["provenance"]["human"] < rules["min_human_pct"]:
        outcome = "blocked"
        reason = "human_pct_below_threshold"
    else:
        outcome = "allowed"
        reason = "policy_passed"

    decision_id = str(uuid.uuid4())

    # 🔐 UAAL HOOK
    authorize_and_record(
        action="apply_veto",
        subject_id=cocreation["id"],
        decision=outcome,
        context=evidence
    )

    return VetoDecision(
        id=decision_id,
        cocreation_id=cocreation["id"],
        policy_id=policy.id,
        outcome=outcome,
        reason=reason,
        evidence=evidence
    )
