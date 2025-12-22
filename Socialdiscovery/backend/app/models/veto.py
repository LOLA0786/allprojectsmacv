from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class VetoDecision(Base):
    __tablename__ = "veto_decisions"

    id = Column(String, primary_key=True)
    cocreation_id = Column(String, index=True)
    policy_id = Column(String)

    outcome = Column(String)   # allowed | blocked | escalated
    reason = Column(String)
    evidence = Column(JSON)    # inputs, thresholds, eval snapshot

    created_at = Column(DateTime, server_default=func.now())
