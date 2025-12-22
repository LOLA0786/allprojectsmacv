from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class AppealResolution(Base):
    __tablename__ = "appeal_resolutions"

    id = Column(String, primary_key=True)
    appeal_id = Column(String, index=True)

    outcome = Column(String)  # revise | escalate | rejected
    votes = Column(Integer)
    resolved_by = Column(String)  # system | quorum | timeout

    created_at = Column(DateTime, server_default=func.now())
