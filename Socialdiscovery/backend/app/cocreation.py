from datetime import datetime
import uuid

COCREATIONS = {}

def create_cocreation(intent_id: str, ai_draft: str):
    cid = str(uuid.uuid4())
    obj = {
        "id": cid,
        "intent_id": intent_id,
        "final_text": ai_draft,
        "history": [
            {"by": "ai", "text": ai_draft, "at": datetime.utcnow().isoformat()}
        ],
        "provenance": {
            "ai": 0.6,
            "human": 0.4
        },
        "vetoed": False
    }
    COCREATIONS[cid] = obj
    return obj

def human_edit(cid: str, text: str):
    if cid not in COCREATIONS:
        return None
    obj = COCREATIONS[cid]
    obj["final_text"] = text
    obj["history"].append(
        {"by": "human", "text": text, "at": datetime.utcnow().isoformat()}
    )
    obj["provenance"]["human"] += 0.2
    obj["provenance"]["ai"] -= 0.2
    return obj

def veto(cid: str, issue: str):
    if cid not in COCREATIONS:
        return None
    obj = COCREATIONS[cid]
    obj["vetoed"] = True
    obj["veto_issue"] = issue
    return obj
