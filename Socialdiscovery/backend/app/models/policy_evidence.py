from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class PolicyEvidence(Base):
    __tablename__ = "policy_evidence"

    id = Column(String, primary_key=True)
    action = Column(String)     # e.g. apply_veto
    subject_id = Column(String)

    decision = Column(String)
    context = Column(JSON)
    hash = Column(String)       # cryptographic digest

    created_at = Column(DateTime, server_default=func.now())
