from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # USER | RESTAURANT | ADMIN
    country = Column(String, nullable=True)
    state = Column(String, nullable=True)


class Bottle(Base):
    __tablename__ = "bottles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    brand = Column(String, nullable=False)
    total_ml = Column(Integer, nullable=False)
    remaining_ml = Column(Integer, nullable=False)


class PourTransaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    bottle_id = Column(String, ForeignKey("bottles.id"), nullable=False)
    restaurant_id = Column(String, nullable=False)
    poured_ml = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
