from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.room_engine import join, leave

router = APIRouter()

rooms = {}

@router.websocket("/room/{moment_id}")
async def room(ws: WebSocket, moment_id: str):
    await ws.accept()

    rooms.setdefault(moment_id, []).append(ws)
    join(moment_id)

    try:
        while True:
            msg = await ws.receive_text()
            for client in rooms.get(moment_id, []):
                await client.send_text(msg)

    except WebSocketDisconnect:
        rooms[moment_id].remove(ws)
        leave(moment_id)

        if not rooms[moment_id]:
            del rooms[moment_id]


@router.websocket("/ws/typing/{room_id}")
async def typing_ws(ws: WebSocket, room_id: str):
    await ws.accept()
    try:
        while True:
            msg = await ws.receive_text()
            await broadcast(room_id, f"typing:{msg}")
    except:
        await ws.close()
