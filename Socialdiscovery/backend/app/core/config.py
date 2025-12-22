import os

POSTGRES_URL = os.getenv(
    "POSTGRES_URL",
    "sqlite:///./dev.db"
)

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)
