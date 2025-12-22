import uuid
from app.uaal import authorize_and_record
from app.models.appeal import Appeal

def submit_appeal(veto_decision, payload):
    appeal = Appeal(
        id=str(uuid.uuid4()),
        veto_decision_id=veto_decision.id,
        cocreation_id=veto_decision.cocreation_id,
        argument=payload["argument"],
        requested_outcome=payload["requested_outcome"],
        authored_by=payload["author"],
        status="open"
    )

    # 🔐 UAAL: record appeal intent
    authorize_and_record(
        action="submit_appeal",
        subject_id=veto_decision.id,
        decision="submitted",
        context={
            "argument": payload["argument"],
            "requested_outcome": payload["requested_outcome"]
        }
    )

    return appeal
