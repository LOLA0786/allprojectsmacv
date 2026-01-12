from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.propagator import OrbitPropagator

app = FastAPI(
    title="KoshaTrack SSA API",
    description="Sovereign Space Situational Awareness Platform",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

propagator = OrbitPropagator()

class TLELoad(BaseModel):
    name: str
    line1: str
    line2: str

class PropagateRequest(BaseModel):
    sat_name: str
    time: Optional[datetime] = None

@app.get("/")
async def root():
    return {
        "name": "KoshaTrack SSA API",
        "version": "0.1.0",
        "status": "operational",
        "satellites_loaded": len(propagator.satellites),
        "message": "India's Sovereign Space Situational Awareness Platform"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/tle/load")
async def load_tle(tle: TLELoad):
    success = propagator.load_tle(tle.name, tle.line1, tle.line2)
    if success:
        return {"status": "success", "satellite": tle.name}
    raise HTTPException(status_code=400, detail="Failed to load TLE")

@app.post("/propagate")
async def propagate(req: PropagateRequest):
    time = req.time or datetime.utcnow()
    try:
        result = propagator.propagate(req.sat_name, time)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/satellites")
async def list_satellites():
    return {
        "count": len(propagator.satellites),
        "satellites": list(propagator.satellites.keys())
    }
