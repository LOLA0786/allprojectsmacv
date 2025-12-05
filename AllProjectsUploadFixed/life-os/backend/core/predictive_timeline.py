import requests
import datetime
from collections import defaultdict, Counter
import re
from statistics import mean

def fetch_events(top_k=1000):
    try:
        r = requests.post("http://0.0.0.0:8000/search/", json={"query":"", "top_k": top_k}, timeout=10)
        r.raise_for_status()
        return r.json() or []
    except Exception:
        return []

def normalize_text(s):
    if not s: return ""
    s = re.sub(r'[^0-9A-Za-z ]+', ' ', s).lower()
    return s

def predict_recurring_events(top_k=1000):
    events = fetch_events(top_k=top_k)
    # group by normalized content signature (very simple)
    groups = defaultdict(list)
    for ev in events:
        doc = ev.get("document","")
        ts = ev.get("timestamp") or ev.get("metadata",{}).get("timestamp")
        if not ts:
            # attempt to parse iso-like strings in metadata
            ts = ev.get("metadata",{}).get("time")
        try:
            ts = int(ts)
        except Exception:
            # fallback to use current time
            ts = int(datetime.datetime.now().timestamp())
        key = normalize_text(doc)[:80]  # signature
        groups[key].append((ts, doc, ev))

    predictions = []
    now_ts = int(datetime.datetime.now().timestamp())
    for sig, items in groups.items():
        if len(items) < 3:
            continue
        # sort by time, compute deltas
        items_sorted = sorted(items, key=lambda x: x[0])
        deltas = []
        for i in range(1, len(items_sorted)):
            deltas.append(items_sorted[i][0] - items_sorted[i-1][0])
        if not deltas:
            continue
        avg_delta = int(mean(deltas))
        last_ts = items_sorted[-1][0]
        next_ts = last_ts + avg_delta
        # only predict if next_ts is in future within sensible window
        if next_ts > now_ts and next_ts - now_ts < 60*60*24*365:  # within 1 year
            predictions.append({
                "signature": sig,
                "example_document": items_sorted[-1][1],
                "last_seen": datetime.datetime.utcfromtimestamp(last_ts).isoformat(),
                "avg_interval_seconds": avg_delta,
                "predicted_next": datetime.datetime.utcfromtimestamp(next_ts).isoformat(),
                "confidence": round(min(0.9, len(items_sorted)/10), 2)
            })
    # sort by confidence / avg_interval_small
    predictions = sorted(predictions, key=lambda x: (-x["confidence"], x["avg_interval_seconds"]))
    return {"predictions": predictions, "count_groups_considered": len(groups)}
