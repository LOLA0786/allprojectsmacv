from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.models import User
from app.core.security import hash_password, verify_password, create_token
from app.models.models import User

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(email: str, password: str, role: str, db: Session = Depends(get_db)):
    user = User(
        email=email,
        password_hash=hash_password(password),
        role=role
    )
    db.add(user)
    db.commit()
    return {"status": "registered"}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": user.id, "role": user.role})
    return {"access_token": token}
