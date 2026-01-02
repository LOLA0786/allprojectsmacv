from sqlalchemy import Column, String, DateTime
from app.models.models import Base
from datetime import datetime
import uuid

class Account(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # USER | RESTAURANT | ADMIN

    country = Column(String, nullable=False)
    state = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
