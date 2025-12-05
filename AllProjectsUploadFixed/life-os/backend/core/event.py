from pydantic import BaseModel
from typing import Dict, Any

class LifeEvent(BaseModel):
    source: str
    type: str
    timestamp: int
    content: str
    metadata: Dict[str, Any]
