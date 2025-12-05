from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/moats", tags=["moats"])

class MoatRunReq(BaseModel):
    input: Optional[str] = None
    top_k: Optional[int] = 200
    granular: Optional[bool] = False

@router.get("/")
async def list_moats():
    modes = [
        "long_term_memory",
        "behavior_graph",
        "passive_recorder",
        "autopilot",
        "predictive_timeline",
        "agent_marketplace",
        "semantic_file_explorer",
        "relationship_memory",
        "ai_therapist",
        "hardware_ready"
    ]
    return {"modes": modes, "status": "ok"}

@router.post("/{mode}/run")
async def run_mode(mode: str, payload: MoatRunReq):
    if mode == "long_term_memory":
        from ..core.long_term_memory import summarize_long_term
        result = summarize_long_term(top_k=payload.top_k or 200, granular=payload.granular)
        return {"status":"ok", "mode":mode, "result": result}

    elif mode == "behavior_graph":
        from ..core.behavior_graph import build_graph, query_node
        if payload.input:
            return {"status":"ok", "mode":mode, "result": query_node(payload.input)}
        else:
            g = build_graph(top_k=payload.top_k or 500)
            return {"status":"ok", "mode":mode, "result": g}

    elif mode == "predictive_timeline":
        from ..core.predictive_timeline import predict_recurring_events
        result = predict_recurring_events(top_k=payload.top_k or 1000)
        return {"status":"ok", "mode":mode, "result": result}

    # simple stubs for other modes
    stubs = {
        "passive_recorder": "Stub: passive recorder acknowledged.",
        "autopilot": "Stub: autopilot action queued.",
        "agent_marketplace": "Stub: listing 3 demo agents.",
        "semantic_file_explorer": "Stub: semantic FS scan.",
        "relationship_memory": "Stub: relationship summary.",
        "ai_therapist": "Stub: mood summary.",
        "hardware_ready": "Stub: hardware OK."
    }

    if mode in stubs:
        return {"status":"ok", "mode":mode, "result": stubs[mode]}

    return {"status":"error", "message": f"unknown mode '{mode}'"}
