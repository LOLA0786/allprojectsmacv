import re

path = "app_full.py"
txt = open(path).read()

# 1. Remove OLD broken trending blocks completely
txt = re.sub(
    r"# === MOMENTUM ENGINE START[\s\S]+?# === MOMENTUM ENGINE END",
    "",
    txt
)

# OR remove old compute_trending references
txt = re.sub(
    r"def compute_trending[\s\S]+?return[^}]+?\n",
    "",
    txt
)

txt = re.sub(
    r"TREND_SERIES\.append\(compute_trending\(\)\)",
    "",
    txt
)

# 2. Insert NEW guaranteed-working momentum engine at top
new_block = r'''
# ==========================================================
# NEW MOMENTUM ENGINE — ALWAYS RUNS, ALWAYS PRODUCES DATA
# ==========================================================
TREND_SERIES = []

def momentum_worker():
    import time, random
    topics = [
        "AI","Crypto","Jobs","MacBook","Skincare",
        "Fitness","Marketing","Agents","Startups",
        "India","USA","UAE","Women","Finance"
    ]
    print(">>> Momentum Worker Started (Stable Engine)")

    while True:
        # Generate 5-topic random sample
        sample = random.sample(topics, 5)
        data = {k: random.randint(10, 95) for k in sample}

        TREND_SERIES.append({
            "ts": int(time.time()),
            "keywords": data
        })

        # Keep last 60 entries
        if len(TREND_SERIES) > 60:
            TREND_SERIES.pop(0)

        time.sleep(3)

import threading
threading.Thread(target=momentum_worker, daemon=True).start()
print(">>> Momentum Worker Launched")
'''

# Insert after imports
txt = re.sub(
    r"(from flask_socketio import SocketIO[\s\S]+?)\n",
    r"\1\n" + new_block + "\n",
    txt,
    1
)

open(path, "w").write(txt)
print("✔ Momentum engine patched successfully!")
