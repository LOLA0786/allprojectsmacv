from app.core.db import engine, Base
from app.models.moment import Moment
from app.models.summary import Summary

Base.metadata.create_all(bind=engine)
print("Postgres tables created")
