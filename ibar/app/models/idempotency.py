from sqlalchemy import Column, String, DateTime
from app.models.models import Base
from datetime import datetime

class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    key = Column(String, primary_key=True)
    scope = Column(String, nullable=False)  # POUR, PURCHASE
    created_at = Column(DateTime, default=datetime.utcnow)
