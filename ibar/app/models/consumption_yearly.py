from sqlalchemy import Column, String, Integer
from app.models.models import Base

class ConsumptionYearly(Base):
    __tablename__ = "consumption_yearly"

    user_id = Column(String, primary_key=True)
    year = Column(Integer, primary_key=True)

    total_ml = Column(Integer, nullable=False)
    total_sessions = Column(Integer, nullable=False)
    max_single_day_ml = Column(Integer, nullable=False)
