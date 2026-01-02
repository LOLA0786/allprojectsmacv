from fastapi import APIRouter, Depends
from app.db.deps import get_db

router = APIRouter(prefix="/restaurant")

@router.get("/transactions")
def list_transactions(db=Depends(get_db)):
    return {
        "message": "Transactions visible here (scoped by restaurant_id)"
    }
