from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "🚀 Mehr Backend is WORKING!", "status": "success"}

@app.get("/api/health")
async def health():
    return {"status": "healthy", "message": "Backend connected successfully!"}

@app.get("/api/executions")
async def get_executions():
    return [
        {
            "id": "test-1",
            "input": "Test customer query",
            "status": "completed", 
            "cost_so_far": 0.05,
            "audit_log": [],
            "agents_completed": ["research_agent", "response_agent"]
        }
    ]

@app.post("/api/workflow/execute")
async def execute_workflow():
    return {
        "id": "new-execution-123",
        "status": "running",
        "message": "Workflow started successfully!",
        "agents_completed": []
    }

@app.get("/api/agent-stats")
async def get_agent_stats():
    return {
        "research_agent": {"tasks_completed": 5, "level": 2},
        "response_agent": {"tasks_completed": 8, "level": 3},
        "compliance_agent": {"tasks_completed": 3, "level": 1}
    }

if __name__ == "__main__":
    print("✅ Starting Mehr Backend...")
    print("🌐 Server: http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)

