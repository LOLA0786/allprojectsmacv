from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from backend.memory.chroma_client import collection

router = APIRouter()
search_router = router

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    id: str
    document: str
    metadata: dict
    distance: float | None = None

@router.post("/", response_model=List[SearchResult])
async def search(req: SearchRequest):
    try:
        results = []

        res = collection.query(
            query_texts=[req.query],
            n_results=req.top_k,
        )

        ids = res["ids"][0]
        docs = res["documents"][0]
        metas = res["metadatas"][0]
        distances = res.get("distances", [[None]*len(ids)])[0]

        for i, _id in enumerate(ids):
            results.append(
                SearchResult(
                    id=_id,
                    document=docs[i],
                    metadata=metas[i],
                    distance=distances[i]
                )
            )

        return results

    except Exception:
        return []
