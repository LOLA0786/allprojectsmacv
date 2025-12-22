from fastapi import APIRouter
from app.services.room_engine import typing_velocity

router = APIRouter(prefix="/typing")

@router.get("/{room_id}")
def get_typing(room_id: str):
    v = typing_velocity(room_id)

    if v > 15:
        level = "HIGH"
    elif v > 5:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "velocity": v,
        "level": level
    }
