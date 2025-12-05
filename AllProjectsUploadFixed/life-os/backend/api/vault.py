from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import os
import uuid
import json

router = APIRouter(prefix="/vault", tags=["vault"])

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "vault_data")
os.makedirs(DATA_DIR, exist_ok=True)

class VaultIngest(BaseModel):
    id: str | None = None
    ciphertext_b64: str  # base64 encrypted payload (client-side)
    metadata: Dict[str, Any] | None = {}

@router.post("/ingest")
async def vault_ingest(payload: VaultIngest):
    """
    Store encrypted blob as-is. Server NEVER decrypts.
    Client must handle encryption / key management.
    """
    try:
        blob_id = payload.id or f"vault_{uuid.uuid4().hex}"
        filepath = os.path.join(DATA_DIR, f"{blob_id}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "id": blob_id,
                "ciphertext_b64": payload.ciphertext_b64,
                "metadata": payload.metadata or {}
            }, f, ensure_ascii=False, indent=2)
        return {"status":"ok","id":blob_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def vault_list():
    """
    List stored ciphertext items (metadata only). Server cannot expose plaintext.
    """
    items = []
    for fn in os.listdir(DATA_DIR):
        if fn.endswith(".json"):
            p = os.path.join(DATA_DIR, fn)
            try:
                with open(p, "r", encoding="utf-8") as f:
                    j = json.load(f)
                    items.append({"id": j.get("id"), "metadata": j.get("metadata", {})})
            except:
                continue
    return {"status":"ok","items": items}
