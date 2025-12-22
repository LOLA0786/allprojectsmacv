from sqlalchemy import Column, String, Integer, Float, JSON
from app.core.db import Base

class Insight(Base):
    __tablename__ = "insights"

    id = Column(String, primary_key=True)
    topic = Column(String, index=True)
    window_start = Column(Float)
    window_end = Column(Float)

    message_count = Column(Integer)
    unique_rooms = Column(Integer)

    key_phrases = Column(JSON)
    sentiment = Column(Float)

    created_at = Column(Float)
