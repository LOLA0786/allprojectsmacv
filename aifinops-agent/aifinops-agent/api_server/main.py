from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/ingest/costs")
def ingest_costs(data: dict):
    return {"received": True}

@app.post("/gpu")
def ingest_gpu(data: dict):
    return {"received": True}

@app.post("/actions/optimize")
def optimize(data: dict):
    return {"status": "pending"}

