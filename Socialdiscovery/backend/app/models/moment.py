import uuid
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.types import JSON
from app.core.db import Base

class Moment(Base):
    __tablename__ = "moments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    intent = Column(String, nullable=False)
    embedding = Column(JSON, nullable=False)
    users = Column(Integer, nullable=False)
    summary = Column(String, nullable=True)

    created_at = Column(Float, nullable=False)
    expires_at = Column(Float, nullable=False)
