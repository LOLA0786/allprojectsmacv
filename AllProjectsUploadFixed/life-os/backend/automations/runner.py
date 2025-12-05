import asyncio
import json
from datetime import datetime
from backend.utils.db import get_unprocessed_events, mark_event_processed, list_automations, add_automation
from backend.utils.db import conn

async def apply_action(event, action: dict):
    content = f"Automation: {action.get('name')} applied to event {event['id']}"
    conn.execute(
        "INSERT INTO events (source, type, timestamp, content, metadata) VALUES (?, ?, ?, ?, ?)",
        ("automation_engine", "automation", int(datetime.now().timestamp()), content, json.dumps({"event":event['id'], "action":action}))
    )
    conn.commit()

async def run_once():
    automations = list_automations()
    if not automations:
        add_automation("Tag Hello", "hello", {"name":"Tag Hello", "description":"tag hello"})
        automations = list_automations()

    events = get_unprocessed_events(limit=100)
    for ev in events:
        for rule in automations:
            if rule["trigger_keyword"].lower() in ev["content"].lower():
                await apply_action(ev, json.loads(rule["action_json"]))
        mark_event_processed(ev["id"])

async def loop_runner(interval_seconds: int = 5):
    while True:
        await run_once()
        await asyncio.sleep(interval_seconds)

if __name__ == "__main__":
    asyncio.run(loop_runner(5))
