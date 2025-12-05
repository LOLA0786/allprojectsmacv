from datetime import datetime
from backend.core.event import LifeEvent
from backend.utils.db import save_event
from backend.memory.indexer import process_event

async def ingest_event(event: LifeEvent):
    # convert pydantic model → dict
    event_dict = event.model_dump()

    # store
    evt_id = save_event(event_dict)

    # vector memory
    await process_event(event_dict)

    return {"status": "ok", "id": evt_id, "received_at": datetime.now().isoformat()}
