from sqlalchemy import Column, String
from app.models.models import Base
import uuid

class Account(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)  # USER | RESTAURANT | ADMIN
    country = Column(String)
    state = Column(String)
