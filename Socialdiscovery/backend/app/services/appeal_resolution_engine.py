import uuid
from datetime import datetime, timedelta
from app.uaal import authorize_and_record
from app.models.appeal_resolution import AppealResolution

def resolve_appeal(appeal, policy, votes):
    rules = policy.rules.get("appeal", {})
    quorum = rules.get("quorum", 1)

    if votes >= quorum:
        outcome = appeal.requested_outcome
        resolved_by = "quorum"
    else:
        outcome = "rejected"
        resolved_by = "policy"

    authorize_and_record(
        action="resolve_appeal",
        subject_id=appeal.id,
        decision=outcome,
        context={
            "votes": votes,
            "quorum": quorum,
            "policy_id": policy.id
        }
    )

    return AppealResolution(
        id=str(uuid.uuid4()),
        appeal_id=appeal.id,
        outcome=outcome,
        votes=votes,
        resolved_by=resolved_by
    )
