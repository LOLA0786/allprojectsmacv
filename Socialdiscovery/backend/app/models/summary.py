from sqlalchemy import Column, String, Float, Text
from app.core.db import Base

class Summary(Base):
    __tablename__ = "summaries"

    moment_id = Column(String, primary_key=True)
    content = Column(Text)
    created_at = Column(Float)
