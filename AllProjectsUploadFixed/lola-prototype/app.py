#!/usr/bin/env python3
"""
LOLA Full Prototype
- Realtime chat (SocketIO)
- SuperConnect (LLM + heuristic)
- Language detection + optional translate
- Product rooms + Marketplace
- Trending momentum timeseries
- Room summarizer (OpenAI optional)
- Anonymous HMAC token for persistent anon ids
Run: python app.py (port 7860)
"""
import os, time, uuid, hmac, hashlib, json, math
from collections import defaultdict, deque, Counter
from flask import Flask, request, jsonify, render_template, abort, send_file
from flask_socketio import SocketIO, join_room, leave_room, emit
from langdetect import detect, DetectorFactory
import requests

DetectorFactory.seed = 0

# Env / config
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
X_API_KEY = os.environ.get("X_API_KEY")
LOLA_HMAC_SECRET = os.environ.get("LOLA_HMAC_SECRET", "localdevsecret_change")
FLASK_SECRET = os.environ.get("FLASK_SECRET", "localflasksecret")

# App init
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = FLASK_SECRET
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# In-memory stores (swap for DB in prod)
ROOMS = {}                # room_id -> metadata
MESSAGES = defaultdict(list)
RECENT = deque(maxlen=2000)
MARKETPLACE = {}          # product_id -> product
USERS = {}                # user_id -> anon_name
TREND_SERIES = deque(maxlen=300)

# Utilities
def now_ts(): return int(time.time())
def newid(prefix="id"): return prefix + uuid.uuid4().hex[:8]
def anon_token(device_str):
    hm = hmac.new(LOLA_HMAC_SECRET.encode(), device_str.encode(), hashlib.sha256).hexdigest()
    return hm[:22]

def add_message(room_id, user, anon, text, mtype="text"):
    msg = {"id": newid("m"), "user": user, "anon": anon, "text": text, "type": mtype, "ts": time.time()}
    MESSAGES[room_id].append(msg)
    RECENT.append(msg)
    # lightweight trending record
    TREND_SERIES.append({"ts": now_ts(), "len": len(RECENT)})
    socketio.emit("new_message", {"room": room_id, "msg": msg}, room=room_id)
    return msg

def extract_keywords(text, n=8):
    words = [w.lower().strip(".,!?()[]{}:;:\\\"'") for w in text.split() if len(w)>2]
    c = Counter(words)
    return [w for w,_ in c.most_common(n)]

# -------------------------
# OpenAI helpers (simple)
# -------------------------
def call_openai_chat(prompt, max_tokens=200, temperature=0.0):
    if not OPENAI_KEY:
        return None
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
        payload = {"model": "gpt-4o-mini", "messages": [{"role":"user","content":prompt}], "max_tokens": max_tokens, "temperature": temperature}
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        if r.status_code == 200:
            j = r.json()
            return j["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("OpenAI error:", e)
    return None

def llm_similarity(a,b):
    # ask LLM for similarity, fallback to simple overlap
    if not OPENAI_KEY:
        return simple_similarity(a,b)
    prompt = f"Rate similarity between these two short phrases from 0 to 1 (single float):\\nA: {a}\\nB: {b}\\nRespond only with the number."
    resp = call_openai_chat(prompt, max_tokens=8, temperature=0.0)
    if resp:
        import re
        m = re.search(r"([0-9]*\\.?[0-9]+)", resp)
        if m:
            try:
                val = float(m.group(1))
                return max(0.0, min(1.0, val))
            except:
                pass
    return simple_similarity(a,b)

def simple_similarity(a,b):
    sa = set([w.lower().strip(".,!?") for w in a.split() if len(w)>2])
    sb = set([w.lower().strip(".,!?") for w in b.split() if len(w)>2])
    if not sa or not sb: return 0.0
    return len(sa & sb) / len(sa | sb)

def generate_room_summary(room_id):
    msgs = MESSAGES.get(room_id, [])[-60:]
    text = "\\n".join(m["text"] for m in msgs if m["type"]=="text")
    if not text.strip():
        return "No discussion yet."
    prompt = "Write a concise 2-line summary of the main points in this conversation:\\n\\n" + text
    resp = call_openai_chat(prompt, max_tokens=120)
    return resp or " ".join(extract_keywords(text, 6))

def translate_text_to(text, target_lang="en"):
    # use OpenAI to translate; fallback no-op
    if not OPENAI_KEY:
        return text
    prompt = f"Translate this to {target_lang} language, keep meaning intact:\\n\\n{text}"
    resp = call_openai_chat(prompt, max_tokens=400)
    return resp or text

# -------------------------
# Seed rooms & marketplace
# -------------------------
def seed_data():
    now = now_ts()
    def mk(title, category="general", tags=None, private=False, product=False, affiliate=None, lang=None):
        rid = newid("r")
        meta = {"id":rid, "title":title, "category":category, "tags":tags or [], "private":private, "product":product, "affiliate":affiliate, "created_at":now, "lang": lang}
        ROOMS[rid] = meta
        return rid
    mk("MacBook Buyers","product",tags=["macbook","apple"], product=True, affiliate="https://example.com/aff/macbook", lang="en")
    mk("AI Agents & Tools","tech",tags=["ai","agents"], lang="en")
    mk("Skincare: Honest Reviews","health",tags=["skincare","beauty"], lang="en")
    mk("Hiring: DeepTech","talent",tags=["hiring","deeptech"], private=True, lang="en")
    # marketplace
    pid = newid("p")
    MARKETPLACE[pid] = {"id":pid, "title":"Protein Powder 500g", "price":699, "affiliate":"https://example.com/aff/protein", "creator":"creator_1"}
seed_data()

# -------------------------
# Routes & APIs
# -------------------------
@app.route("/")
def index():
    # trending keywords
    recent_text = " ".join(m["text"] for m in list(RECENT)[-800:])
    trending = extract_keywords(recent_text, 12)
    rooms = sorted(ROOMS.values(), key=lambda r: r["created_at"], reverse=True)
    products = list(MARKETPLACE.values())
    return render_template("index.html", trending=trending, rooms=rooms, marketplace=products)

@app.route("/room/<rid>")
def room_view(rid):
    r = ROOMS.get(rid)
    if not r:
        abort(404)
    summary = generate_room_summary(rid) if OPENAI_KEY else None
    return render_template("room.html", room=r, summary=summary)

@app.route("/dashboard")
def dashboard():
    total_msgs = sum(len(v) for v in MESSAGES.values())
    total_rooms = len(ROOMS)
    return render_template("dashboard.html", total_msgs=total_msgs, total_rooms=total_rooms, rooms=ROOMS.values())

@app.route("/marketplace")
def marketplace():
    return render_template("marketplace.html", products=list(MARKETPLACE.values()))

@app.route("/api/rooms", methods=["GET","POST"])
def api_rooms():
    if request.method == "GET":
        return jsonify(list(ROOMS.values()))
    data = request.json or {}
    title = data.get("title","Untitled")
    category = data.get("category","general")
    tags = data.get("tags",[])
    lang = None
    try:
        lang = detect(title)
        tags.append("lang:" + lang)
    except:
        pass
    rid = newid("r")
    ROOMS[rid] = {"id":rid,"title":title,"category":category,"tags":tags,"private":data.get("private",False),"product":data.get("product",False),"affiliate":data.get("affiliate"),"created_at": now_ts(), "lang": lang}
    return jsonify({"ok":True,"room":ROOMS[rid]})

@app.route("/api/messages/<rid>", methods=["GET"])
def api_messages(rid):
    after = float(request.args.get("after",0))
    msgs = [m for m in MESSAGES.get(rid, []) if m["ts"]>after]
    return jsonify({"messages":msgs, "now": time.time()})

@app.route("/api/marketplace", methods=["GET","POST"])
def api_marketplace():
    if request.method == "GET":
        return jsonify(list(MARKETPLACE.values()))
    data = request.json or {}
    pid = newid("p")
    MARKETPLACE[pid] = {"id":pid,"title":data.get("title"),"price":data.get("price",0),"affiliate":data.get("affiliate")}
    return jsonify({"ok":True,"product": MARKETPLACE[pid]})

@app.route("/api/trending_timeseries", methods=["GET"])
def api_trending_series():
    # return simple series of last N TREND_SERIES points
    return jsonify({"series": list(TREND_SERIES)[-120:]})

@app.route("/api/superconnect", methods=["POST"])
def api_superconnect():
    data = request.json or {}
    user_id = data.get("user") or newid("u")
    intent = data.get("intent","").strip()
    if not intent:
        return jsonify({"ok":False,"error":"no_intent"})
    # candidate pool from RECENT messages (fast)
    last_per_user = {}
    for m in reversed(list(RECENT)[-800:]):
        if m["user"] not in last_per_user:
            last_per_user[m["user"]] = m["text"]
    best = None
    best_score = 0.0
    for uid, text in last_per_user.items():
        if uid == user_id: continue
        # LLM boost if available
        score = simple_similarity(intent, text)
        if OPENAI_KEY:
            try:
                score = max(score, llm_similarity(intent, text))
            except Exception:
                pass
        if score > best_score:
            best_score = score
            best = uid
    if not best or best_score < 0.12:
        return jsonify({"ok":False,"reason":"no_match","score":best_score})
    # create private room
    rid = newid("r")
    ROOMS[rid] = {"id":rid,"title": f"SuperConnect {user_id[:6]}↔{best[:6]}", "category":"match", "tags":["match"], "private":True, "created_at": now_ts()}
    # generate intro summary using LLM if available
    intro = "You have been matched. Say hi!"
    if OPENAI_KEY:
        try:
            intro = generate_room_summary(rid) or intro
        except Exception:
            pass
    add_message(rid, "system", "system", f"Matched users. Intro: {intro}", "system")
    return jsonify({"ok":True, "room": rid, "match_user": best, "score": best_score})

# -------------------------
# SocketIO events
# -------------------------
@socketio.on("join")
def on_join(data):
    room = data.get("room")
    user = data.get("user") or newid("u")
    anon = data.get("anon") or anon_token(request.headers.get("User-Agent","unknown")+str(time.time()))
    join_room(room)
    add_message(room, user, anon, "joined the room", "system")
    emit("joined_ack", {"room":room, "user":user, "anon":anon})

@socketio.on("leave")
def on_leave(data):
    room = data.get("room")
    user = data.get("user")
    leave_room(room)
    add_message(room, user or "anon", "system", "left the room", "system")

@socketio.on("send")
def on_send(data):
    room = data.get("room")
    user = data.get("user") or newid("u")
    anon = data.get("anon") or anon_token(request.headers.get("User-Agent","unknown")+str(time.time()))
    text = data.get("text","")
    mtype = data.get("type","text")
    m = add_message(room, user, anon, text, mtype)
    emit("sent_ack", {"ok":True, "msg": m}, room=room)

# Health
@app.route("/health")
def health():
    return jsonify({"ok":True, "time": now_ts()})

# Background trending sampler (non-blocking)
def trending_worker():
    while True:
        try:
            blob = " ".join(m["text"] for m in list(RECENT)[-800:])
            kws = extract_keywords(blob, 10)
            TREND_SERIES.append({"ts": now_ts(), "keywords": kws, "count": len(blob.split())})
        except Exception:
            pass
        time.sleep(6)

# start background worker
import threading
t = threading.Thread(target=trending_worker, daemon=True)
t.start()

if __name__ == "__main__":
    print("LOLA Full Prototype running on http://0.0.0.0:7860")
    socketio.run(app, host="0.0.0.0", port=7860)
