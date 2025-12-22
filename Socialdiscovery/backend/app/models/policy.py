from sqlalchemy import Column, String, Integer, JSON, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Policy(Base):
    __tablename__ = "policies"

    id = Column(String, primary_key=True)
    scope = Column(String, index=True)  # e.g. hub:ai-governance
    rules = Column(JSON)                # declarative constraints
    version = Column(Integer, default=1)
    active = Column(Boolean, default=True)

    authored_by = Column(JSON)           # list of user ids
    signed = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
