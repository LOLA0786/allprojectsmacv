from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Appeal(Base):
    __tablename__ = "appeals"

    id = Column(String, primary_key=True)
    veto_decision_id = Column(String, index=True)
    cocreation_id = Column(String, index=True)

    argument = Column(String)        # human-written explanation
    requested_outcome = Column(String)  # allow | revise | escalate

    status = Column(String, default="open")  
    # open | accepted | rejected | escalated

    authored_by = Column(String)
    created_at = Column(DateTime, server_default=func.now())
