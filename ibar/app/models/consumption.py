from sqlalchemy import Column, String, Integer
from app.models.models import Base

class ConsumptionSummary(Base):
    __tablename__ = "consumption_summary"

    user_id = Column(String, primary_key=True)
    year = Column(Integer, primary_key=True)

    total_ml = Column(Integer)
    total_sessions = Column(Integer)
    max_single_day_ml = Column(Integer)
    avg_ml_per_session = Column(Integer)
