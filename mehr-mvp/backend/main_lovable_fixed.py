from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import json
from datetime import datetime
import asyncio
import random
import uvicorn

app = FastAPI(title="Mehr Lovable Platform", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== LOVABLE FEATURES ====================

AGENT_PERSONALITIES = {
    "research_agent": {"name": "Sherlock", "emoji": "🔍", "color": "#3B82F6"},
    "response_agent": {"name": "Joy", "emoji": "💖", "color": "#10B981"},
    "compliance_agent": {"name": "Guardian", "emoji": "🛡️", "color": "#8B5CF6"}
}

AGENT_BANTER = [
    "Hey team, I've analyzed the situation!",
    "This one needs our collaborative magic! ✨", 
    "Working together makes us unstoppable!",
    "Another happy customer in the making! 🎉"
]

agent_stats = {
    "research_agent": {"tasks_completed": 12, "level": 2},
    "response_agent": {"tasks_completed": 18, "level": 3}, 
    "compliance_agent": {"tasks_completed": 8, "level": 1}
}

ACHIEVEMENTS = {
    "first_workflow": {"name": "🚀 First Flight", "unlocked": True},
    "team_player": {"name": "🤝 Team Player", "unlocked": True},
    "customer_whisperer": {"name": "💝 Customer Whisperer", "unlocked": False}
}

class WorkflowRequest(BaseModel):
    user_input: str
    language: str = "english"

executions_db = {}

def get_current_time():
    return datetime.now().isoformat()

@app.post("/api/workflow/execute")
async def execute_workflow(request: WorkflowRequest, background_tasks: BackgroundTasks):
    execution_id = str(uuid.uuid4())
    
    emotion_data = {
        "primary_emotion": random.choice(["frustrated", "happy", "confused", "neutral"]),
        "emotion_emoji": random.choice(["😠", "😊", "😕", "😐"])
    }
    
    execution = {
        "id": execution_id,
        "input": request.user_input,
        "status": "running",
        "created_at": get_current_time(),
        "audit_log": [],
        "agents_completed": [],
        "emotion_detected": emotion_data,
        "personality_messages": [],
        "banter_messages": [],
        "language": request.language
    }
    
    # Add personality messages
    for agent_id, personality in AGENT_PERSONALITIES.items():
        execution["personality_messages"].append({
            "agent": agent_id,
            "message": f"{personality['emoji']} {personality['name']} is on the case!",
            "type": "welcome",
            "timestamp": get_current_time()
        })
    
    executions_db[execution_id] = execution
    
    background_tasks.add_task(simulate_workflow, execution_id)
    
    return execution

async def simulate_workflow(execution_id: str):
    execution = executions_db[execution_id]
    
    # Research Agent
    await asyncio.sleep(1)
    execution["audit_log"].append({
        "agent": "research_agent",
        "action": "research_completed", 
        "result": {"key_facts": ["Analyzed customer query"], "needs_human_approval": False},
        "timestamp": get_current_time()
    })
    execution["agents_completed"].append("research_agent")
    
    # Banter
    execution["banter_messages"].append({
        "from_agent": "research_agent",
        "to_agent": "response_agent",
        "message": random.choice(["Joy, your turn to add some warmth! 💖", "Ready for your empathy magic!"]),
        "timestamp": get_current_time()
    })
    
    # Response Agent  
    await asyncio.sleep(1)
    execution["audit_log"].append({
        "agent": "response_agent",
        "action": "response_generated",
        "result": {"response": "Crafted a caring response", "tone": "empathetic"},
        "timestamp": get_current_time()
    })
    execution["agents_completed"].append("response_agent")
    
    # More banter
    execution["banter_messages"].append({
        "from_agent": "response_agent", 
        "to_agent": "compliance_agent",
        "message": "Guardian, mind checking this for compliance? 🛡️",
        "timestamp": get_current_time()
    })
    
    # Compliance Agent
    await asyncio.sleep(1)
    execution["audit_log"].append({
        "agent": "compliance_agent",
        "action": "compliance_checked",
        "result": {"is_compliant": True, "risk_level": "low"},
        "timestamp": get_current_time()
    })
    execution["agents_completed"].append("compliance_agent")
    
    # Final celebration
    execution["banter_messages"].append({
        "from_agent": "system",
        "message": random.choice(AGENT_BANTER),
        "type": "celebration",
        "timestamp": get_current_time()
    })
    
    execution["status"] = "completed"
    execution["final_output"] = {"message": "Success! All agents completed their tasks! 🎉"}

@app.get("/api/executions")
async def get_executions():
    return list(executions_db.values())

@app.get("/api/agent-stats")
async def get_agent_stats():
    return agent_stats

@app.get("/api/achievements") 
async def get_achievements():
    return ACHIEVEMENTS

@app.get("/api/agent-personalities")
async def get_agent_personalities():
    return AGENT_PERSONALITIES

@app.get("/api/workflow-recipes")
async def get_workflow_recipes():
    return {
        "refund_request": {"name": "💰 Refund Request", "emoji": "💰"},
        "complaint_resolution": {"name": "😤 Complaint Resolution", "emoji": "😤"},
        "information_request": {"name": "🤔 Information Request", "emoji": "🤔"}
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0", "features": "Lovable Platform"}

if __name__ == "__main__":
    print("🚀💝 Starting LOVABLE Mehr Platform...")
    print("✨ Features: Personalities, Banter, Emotions, Levels, Achievements!")
    print("🌐 Server: http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
