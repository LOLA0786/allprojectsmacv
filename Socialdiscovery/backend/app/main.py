from fastapi import FastAPI

from app.api.intent import router as intent_router
from app.api.cocreation import router as cocreation_router
from app.api.appeals import router as appeal_router
from app.api.appeal_resolution import router as appeal_resolution_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(intent_router)
app.include_router(cocreation_router)
app.include_router(appeal_router)
app.include_router(appeal_resolution_router)
