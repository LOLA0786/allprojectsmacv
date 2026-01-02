from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.bottles import router as bottles_router
from app.api.pos import router as pos_router
from app.api.analytics import router as analytics_router

app = FastAPI(title="iBar Backend", version="0.1")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(bottles_router)
app.include_router(pos_router)
app.include_router(analytics_router)
