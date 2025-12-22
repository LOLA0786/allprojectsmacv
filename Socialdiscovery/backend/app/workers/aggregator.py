# ---- BOOTSTRAP IMPORT PATH (DO NOT REMOVE) ----
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# ----------------------------------------------

from app.core.redis import redis_client
from app.core.db import SessionLocal
from app.services.aggregate_job import run_aggregation
import json
import time

STREAM = "events"
GROUP = "aggregators"
CONSUMER = "worker-1"

def main():
    try:
        redis_client.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
    except Exception:
        pass

    while True:
        msgs = redis_client.xreadgroup(
            GROUP,
            CONSUMER,
            {STREAM: ">"},
            count=10,
            block=5000
        )

        for stream, events in msgs:
            for msg_id, data in events:
                event_type = data.get("type")
                payload = json.loads(data.get("payload", "{}"))

                if event_type == "intent_processed":
                    db = SessionLocal()
                    run_aggregation(
                        db,
                        summaries=["example summary"] * 30,
                        topic=payload.get("intent", "unknown")
                    )
                    db.close()

                redis_client.xack(STREAM, GROUP, msg_id)

        time.sleep(0.1)

if __name__ == "__main__":
    main()
