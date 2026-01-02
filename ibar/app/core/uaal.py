def authorize_pour(context: dict):
    # Stub now, real UAAL later
    # context = user, location, ml, velocity, history
    if context["ml"] > context.get("max_ml", 90):
        return {"decision": "BLOCK", "reason": "LIMIT_EXCEEDED"}

    return {"decision": "ALLOW", "evidence_id": "0xUAAL123"}
