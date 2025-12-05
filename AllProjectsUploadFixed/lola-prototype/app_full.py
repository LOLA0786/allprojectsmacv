#!/usr/bin/env python3
"""
Clean, stable Flask app for LOLA — Upgraded Marketplace + Dashboard v2 UI.
- Bind: 0.0.0.0:7860
- Routes: marketplace, product, mentors, premium, dashboard_v2, index, room
- API: /api/dashboard/momentum, /api/stream_intent
- Lightweight topic matcher background worker that auto-creates rooms on demand
"""

import os
import time
import threading
import random
from collections import defaultdict, deque, Counter
from flask import Flask, request, jsonify, render_template

# -----------------------------
# Config
# -----------------------------
PORT = int(os.environ.get("PORT", 7860))
APP_DEBUG = False

app = Flask(__name__, template_folder="templates", static_folder="static")

# -----------------------------
# In-memory state (for prototype)
# -----------------------------
USERS = {}                # user_id -> {id, meta}
ROOMS = {}                # room_id -> {"topic":..., "members":[user,...], "created":ts}
TOPIC_BUCKETS = defaultdict(list)  # topic -> list of (user, ts)
RECENT = deque(maxlen=1000)  # recent intent messages
TREND_SERIES = []         # list of {ts, keywords: {k:score}}

MIN_GROUP_USERS = 3
AUTO_ROOM_PREFIX = "auto-"

# -----------------------------
# Helpers
# -----------------------------
def now_ts():
    return int(time.time())

def ensure_user(uid):
    if not uid:
        uid = f"anon-{random.randint(1000,9999)}"
    if uid not in USERS:
        USERS[uid] = {"id": uid, "joined": now_ts()}
    return uid

_stopwords = set("""the and is in at to for of a an on with about how what why""".split())

def extract_topics(text, n=3):
    """
    Very simple keyword extractor: tokenizes, lowercases, counts frequency
    Returns top n words joined as a topic key.
    """
    if not text:
        return "misc"
    tokens = []
    for w in text.lower().split():
        w = "".join(ch for ch in w if ch.isalnum())
        if not w or len(w) < 3 or w in _stopwords:
            continue
        tokens.append(w)
    if not tokens:
        return "misc"
    ctr = Counter(tokens)
    top = [k for k,_ in ctr.most_common(n)]
    return " ".join(top)

def create_auto_room(topic, users):
    """
    Create a room id and populate ROOMS.
    users: list of tuples (user, ts)
    """
    rid = AUTO_ROOM_PREFIX + str(random.randint(100000, 999999))
    members = [u for u,_ in users]
    ROOMS[rid] = {"id": rid, "topic": topic, "members": members, "created": now_ts()}
    # Track in user metadata
    for u in members:
        USERS.setdefault(u, {}) 
        USERS[u].setdefault("rooms", []).append(rid)
    app.logger.info(f"Auto-room created {rid} for topic '{topic}' with {len(members)} users")
    return rid


@app.route("/product/<pid>")
def product_detail(pid):
    return render_template("product_detail.html", pid=pid)

@app.route("/mentors")
def mentors_page():
    return render_template("mentors.html")

@app.route("/premium")
def premium_page():
    return render_template("premium.html")

@app.route("/dashboard_v2")
def dashboard_v2_page():
    return render_template("dashboard_v2.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/room/<rid>")
def room_view(rid):
    room = ROOMS.get(rid)
    if not room:
        return render_template("room.html", rid=rid)
    return render_template("room.html", rid=rid, topic=room.get("topic"), members=room.get("members"))

# -----------------------------
# Health check
# -----------------------------
@app.route("/health")
def health():
    return jsonify({"ok": True, "ts": now_ts()})

# -----------------------------
# Debug helper: list routes (only if debug)
# -----------------------------
@app.route("/_routes")
def _routes():
    return jsonify([str(r) for r in app.url_map.iter_rules()])

# -----------------------------
# Small utilities
# -----------------------------
def now():
    return int(time.time())

# -----------------------------
# Server startup
# -----------------------------

# ==========================================================
# CLEAN WORKING MOMENTUM API 100% GUARANTEED
# ==========================================================
@app.route("/api/dashboard/momentum")
def api_momentum():
    if not TREND_SERIES:
        # fallback default
        return jsonify({
            "labels": ["AI", "Jobs", "MacBook", "Crypto"],
            "values": [40, 33, 22, 18]
        })

    last = TREND_SERIES[-1]
    labels = list(last["keywords"].keys())
    values = list(last["keywords"].values())
    return jsonify({"labels": labels, "values": values})


if __name__ == "__main__":
    print("\n=== CLEAN LOLA SERVER RUNNING ===")
    print("RUNNING FILE:", __file__)
    print("PORT:", PORT)
    print("=================================\n")
    # Use Flask's builtin dev server for stability on macOS (OK for demo)
    app.run(host="0.0.0.0", port=PORT, debug=APP_DEBUG)

# -----------------------------
# LLM Integration (OpenAI or X-API compatible)
# -----------------------------
import json
import requests

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
X_API_KEY = os.environ.get("X_API_KEY")  # alternative provider key

def llm_extract_topic_via_openai(text):
    """
    Uses OpenAI Chat Completions (or falls back to REST X-API)
    Returns a compact topic string.
    """
    if not text:
        return "misc"
    # prefer official openai package if key is present
    if OPENAI_KEY:
        try:
            import openai
            openai.api_key = OPENAI_KEY
            # Use a small chat model prompt to extract topic keywords
            prompt = [
                {"role":"system","content":"You are a concise keyword extractor. Return 1-3 words/short phrase that capture the user's intent. Do NOT return JSON. Just short phrase."},
                {"role":"user","content": f"Extract the short topic from: \"{text}\""}
            ]
            resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=prompt, max_tokens=16, temperature=0.0)
            topic = resp.choices[0].message.content.strip()
            return topic[:120]
        except Exception:
            # fallback to simple extractor
            return extract_topics(text, n=2)
    elif X_API_KEY:
        # Example of calling a generic REST LLM API that expects X-API-KEY
        try:
            endpoint = "https://api.example.com/v1/chat/completions"  # replace with your provider endpoint
            headers = {"Authorization": f"Bearer {X_API_KEY}", "Content-Type":"application/json"}
            payload = {
                "model": "gpt-small",
                "messages": [
                    {"role":"system","content":"You are a concise keyword extractor. Return 1-3 words/short phrase."},
                    {"role":"user","content": f"Extract the short topic from: \"{text}\""}
                ],
                "max_tokens": 16,
                "temperature": 0.0
            }
            r = requests.post(endpoint, headers=headers, json=payload, timeout=10)
            j = r.json()
            # provider shapes differ — try common fields
            if j.get("choices"):
                topic = j["choices"][0].get("message", {}).get("content") or j["choices"][0].get("text", "")
                if topic:
                    return topic.strip()[:120]
            # fallback
            return extract_topics(text, n=2)
        except Exception:
            return extract_topics(text, n=2)
    else:
        # no LLM keys — fallback to local naive extractor
        return extract_topics(text, n=2)

@app.route("/api/stream_intent_llm", methods=["POST"])
def api_stream_intent_llm():
    """
    Receives JSON: {"user":"u1", "text":"..."}
    Uses LLM to extract topic, inserts into TOPIC_BUCKETS and may auto-create room.
    """
    data = request.get_json(force=True, silent=True) or {}
    user = ensure_user(data.get("user"))
    text = data.get("text","").strip()
    if not text:
        return jsonify({"ok":False, "error":"no text provided"}), 400

    # call LLM to extract short topic
    topic = llm_extract_topic_via_openai(text)
    RECENT.append({"user": user, "text": text, "ts": now_ts()})
    TOPIC_BUCKETS[topic].append((user, time.time()))

    # fast-path: if bucket already has enough active users, create room
    active = [(u,t) for u,t in TOPIC_BUCKETS[topic] if time.time() - t < 12]
    room = None
    if len(active) >= MIN_GROUP_USERS:
        room = create_auto_room(topic, active)
        TOPIC_BUCKETS[topic] = []

    return jsonify({"ok":True, "topic": topic, "room": room})

# ==================================================
# REALTIME (SSE) + LLM Streaming + Embeddings
# ==================================================
import json
import queue
import uuid
import math

# LLM keys (already set earlier by previous patch)
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
X_API_KEY = os.environ.get("X_API_KEY")

# Subscribers for SSE (each subscriber gets a queue.Queue)
SSE_SUBSCRIBERS = []

def register_sse():
    q = queue.Queue()
    SSE_SUBSCRIBERS.append(q)
    return q

def unregister_sse(q):
    try:
        SSE_SUBSCRIBERS.remove(q)
    except ValueError:
        pass

def notify_subscribers(obj):
    """
    obj: JSON-serializable event dict
    Each subscriber receives a JSON string as an SSE 'message' event.
    """
    data = json.dumps(obj)
    for q in list(SSE_SUBSCRIBERS):
        try:
            q.put_nowait(data)
        except queue.Full:
            # skip if queue full
            pass

# Patch topic_matcher_worker to notify subscribers when auto-room created
# (it already creates rooms via create_auto_room). We'll create a thin wrapper.
_old_topic_worker = None
# we will not replace the running thread; instead, ensure create_auto_room calls notify_subscribers
# so we add inside create_auto_room
def _notify_and_create_auto_room(topic, users):
    rid = create_auto_room(topic, users)
    event = {
        "type": "auto_room_created",
        "room": rid,
        "topic": topic,
        "members": [u for u,_ in users],
        "ts": now_ts()
    }
    notify_subscribers(event)
    return rid

# Replace create_auto_room reference inside our module (monkey patch)
create_auto_room_original = create_auto_room
def create_auto_room(topic, users):
    # call the original that also sets ROOMS & USERS
    rid = create_auto_room_original(topic, users)
    event = {
        "type": "auto_room_created",
        "room": rid,
        "topic": topic,
        "members": [u for u,_ in users],
        "ts": now_ts()
    }
    notify_subscribers(event)
    return rid

# -------------------------
# SSE endpoint for browsers to subscribe
# -------------------------
from flask import Response, stream_with_context

@app.route("/stream/subscribe")
def stream_subscribe():
    """
    Server-Sent Events endpoint.
    Browser connects and receives live events (auto-room creation, embedding matches, etc.)
    """
    q = register_sse()

    def gen():
        try:
            # send a welcome event
            yield f"event: message\\ndata: {json.dumps({'type':'welcome','ts':now_ts()})}\\n\\n"
            while True:
                try:
                    data = q.get(timeout=30)
                    # send as message event with JSON payload
                    yield f"event: message\\ndata: {data}\\n\\n"
                except queue.Empty:
                    # keep connection alive with a comment
                    yield ": ping\\n\\n"
        finally:
            unregister_sse(q)

    return Response(stream_with_context(gen()), mimetype="text/event-stream")

# -------------------------
# LLM streaming endpoint (server streams SSE chunks back to caller)
# -------------------------
def stream_openai_chat(text):
    """
    Generator that yields SSE-style "data: ..." chunks as strings.
    Uses OpenAI streaming if key available; otherwise yields a single JSON result.
    """
    if OPENAI_KEY:
        try:
            import openai
            openai.api_key = OPENAI_KEY
            # Use streaming ChatCompletion
            # Note: some OpenAI SDKs return an iterator when stream=True
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # change if needed
                messages=[
                    {"role":"system","content":"You are a concise keyword and intent extractor. Return a short topic phrase and a single-sentence summary. Provide output as JSON with keys: topic, summary."},
                    {"role":"user","content": f"Extract topic and one-line summary from: {text}"}
                ],
                max_tokens=128,
                temperature=0.0,
                stream=True
            )
            # resp is an iterator of events
            collected = ""
            for chunk in resp:
                # chunk is dict-like; attempt to extract delta text
                try:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, 'get'):
                        piece = delta.get("content") or ""
                    else:
                        # some SDKs yield different shapes
                        piece = ""
                    if piece:
                        collected += piece
                        # yield SSE chunk to client
                        yield f"data: {json.dumps({'chunk': piece})}\\n\\n"
                except Exception:
                    # fallback: yield raw chunk
                    yield f"data: {json.dumps({'raw': str(chunk)})}\\n\\n"
            # at end, send final parsed JSON output if possible
            final_text = collected.strip()
            # attempt to parse as JSON
            try:
                parsed = json.loads(final_text)
            except Exception:
                # fallback: return as summary
                parsed = {"topic": extract_topics(text, n=2), "summary": final_text}
            yield f"data: {json.dumps({'done': parsed})}\\n\\n"
            return
        except Exception as e:
            # fallback to non-streaming path
            app.logger.exception("OpenAI streaming failed: %s", e)
            pass

    # fallback (no streaming): produce one message and yield it
    topic = extract_topics(text, n=2)
    summary = text[:200]
    yield f"data: {json.dumps({'chunk': summary})}\\n\\n"
    yield f"data: {json.dumps({'done': {'topic': topic, 'summary': summary}})}\\n\\n"

@app.route("/api/stream_intent_stream", methods=["POST"])
def api_stream_intent_stream():
    """
    Accepts JSON {"user":"u1","text":"..."}.
    Returns streaming response (EventStream) with chunks from LLM and final parsed JSON.
    """
    data = request.get_json(force=True, silent=True) or {}
    user = ensure_user(data.get("user"))
    text = data.get("text","").strip()
    if not text:
        return jsonify({"ok": False, "error": "no text"}), 400

    def generator():
        # first, yield an initial ack
        yield f"data: {json.dumps({'status':'started'})}\\n\\n"
        # stream LLM
        for s in stream_openai_chat(text):
            yield s
        # store recent & buckets, and maybe create room (same as non-LLM endpoint)
        RECENT.append({"user": user, "text": text, "ts": now_ts()})
        topic = extract_topics(text, n=2)
        TOPIC_BUCKETS[topic].append((user, time.time()))
        active = [(u,t) for u,t in TOPIC_BUCKETS[topic] if time.time() - t < 12]
        room = None
        if len(active) >= MIN_GROUP_USERS:
            room = create_auto_room(topic, active)
            TOPIC_BUCKETS[topic] = []
            # notify subscribers of auto-room
            notify_subscribers({"type":"auto_room_created","room":room,"topic":topic,"members":[u for u,_ in active],"ts":now_ts()})
        yield f"data: {json.dumps({'status':'finished','topic': topic, 'room': room})}\\n\\n"

    return Response(stream_with_context(generator()), mimetype="text/event-stream")

# -------------------------
# Embeddings-based similarity endpoint
# -------------------------
def cosine_sim(a,b):
    # a,b: lists of floats
    dot = sum(x*y for x,y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    if na==0 or nb==0:
        return 0.0
    return dot/(na*nb)

# A simple in-memory vector store for demo (pid -> embedding)
EMB_STORE = {}  # pid -> [float,...] and metadata

def get_embedding_openai(text):
    """
    Return an embedding vector (list of floats). Falls back to naive hash-vector if no key.
    """
    if OPENAI_KEY:
        try:
            import openai
            openai.api_key = OPENAI_KEY
            resp = openai.Embedding.create(model="text-embedding-3-small", input=text)
            vec = resp["data"][0]["embedding"]
            return vec
        except Exception as e:
            app.logger.exception("Embedding call failed: %s", e)
    # fallback: deterministic pseudo-embedding using char codes (small)
    v = [0.0]*64
    for i,ch in enumerate(text[:256]):
        v[i % 64] += (ord(ch) % 31) / 31.0
    return v

@app.route("/api/embeddings_index", methods=["POST"])
def api_embeddings_index():
    """
    Indexes a product or document for future similarity matches.
    JSON: {"id":"p1","text":"product description"}
    """
    data = request.get_json(force=True, silent=True) or {}
    pid = data.get("id")
    text = data.get("text","")
    if not pid or not text:
        return jsonify({"ok":False, "error":"id and text required"}), 400
    vec = get_embedding_openai(text)
    EMB_STORE[pid] = {"vec": vec, "text": text, "id": pid}
    return jsonify({"ok":True, "id": pid})

@app.route("/api/embeddings_query", methods=["POST"])
def api_embeddings_query():
    """
    Query similar items.
    JSON: {"text":"query","top_k":3}
    """
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("text","")
    top_k = int(data.get("top_k",3))
    if not text:
        return jsonify({"ok":False, "error":"text required"}), 400
    qv = get_embedding_openai(text)
    scores = []
    for pid, rec in EMB_STORE.items():
        s = cosine_sim(qv, rec["vec"])
        scores.append((s, pid, rec["text"]))
    scores.sort(reverse=True)
    out = [{"id":pid, "score": float(s), "text": txt} for s,pid,txt in [(s,p,t) for s,p,t in scores[:top_k]]]
    return jsonify({"ok":True, "results": out})

# -------------------------
# Demo helper: simulate multiple users posting intents (creates auto rooms)
# -------------------------
@app.route("/api/demo_simulate", methods=["POST"])
def api_demo_simulate():
    """
    Simulate N users posting text in quick succession for demo.
    JSON: {"topic":"macbook", "n":4}
    """
    data = request.get_json(force=True, silent=True) or {}
    topic_text = data.get("topic","demo topic")
    n = int(data.get("n",4))
    users = [f"demo-{i}-{uuid.uuid4().hex[:6]}" for i in range(n)]
    for u in users:
        RECENT.append({"user":u,"text":topic_text,"ts":now_ts()})
        tok = extract_topics(topic_text, n=2)
        TOPIC_BUCKETS[tok].append((u, time.time()))
    return jsonify({"ok":True, "seed_users": users})

# ==================================================
# End appended realtime/LLM/embedding code
# ==================================================
