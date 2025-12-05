from fastapi import FastAPI
from backend.core.event import LifeEvent
from backend.core.ingest import ingest_event
from backend.api.search import search_router
from backend.api.moats import router as moats_router

app = FastAPI(title="Life OS Backend", version="0.1.0")

@app.get("/")
def root():
    return {"status": "ok", "service": "life-os backend"}

# INGEST ENDPOINT
@app.post("/ingest")
async def ingest_api(event: LifeEvent):
    return await ingest_event(event)

# SEARCH ROUTER
app.include_router(search_router)

# MOATS ROUTER
app.include_router(moats_router)

# Vault (encrypted storage) router
from backend.api.vault import router as vault_router
app.include_router(vault_router)
