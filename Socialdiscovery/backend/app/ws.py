from fastapi import WebSocket

HUBS = {}

async def connect_hub(hub_id: str, websocket: WebSocket):
    await websocket.accept()
    HUBS.setdefault(hub_id, []).append(websocket)

def disconnect_hub(hub_id: str, websocket: WebSocket):
    if hub_id in HUBS and websocket in HUBS[hub_id]:
        HUBS[hub_id].remove(websocket)

async def broadcast(hub_id: str, message: dict):
    for ws in HUBS.get(hub_id, []):
        await ws.send_json(message)
