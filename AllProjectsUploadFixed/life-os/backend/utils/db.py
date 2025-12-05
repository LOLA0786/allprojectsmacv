import sqlite3
import json
import os
from typing import Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "timeline.db")

def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id TEXT PRIMARY KEY,
        source TEXT,
        type TEXT,
        timestamp INTEGER,
        content TEXT,
        metadata TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_event(event: Dict[str, Any]) -> str:
    evt_id = event.get("id") or f"evt_{event.get('timestamp','')}_{abs(hash(event.get('content','')))%1000000}"
    metadata = json.dumps(event.get("metadata") or {})

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT OR REPLACE INTO events (id, source, type, timestamp, content, metadata)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        evt_id,
        event.get("source"),
        event.get("type"),
        int(event.get("timestamp") or 0),
        event.get("content"),
        metadata
    ))
    conn.commit()
    conn.close()
    return evt_id

def list_events(limit=1000, since_ts=0):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events WHERE timestamp >= ? ORDER BY timestamp DESC LIMIT ?", (since_ts, limit))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_events():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events ORDER BY timestamp ASC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
