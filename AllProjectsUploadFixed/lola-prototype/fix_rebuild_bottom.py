path = "app_full.py"

with open(path) as f:
    lines = f.readlines()

# keep ONLY lines before 140 (your top server logic is fine)
clean = lines[:140]

# append a brand-new VALID bottom half:
clean.append('''

# ==========================================================
# CLEAN UI ROUTES
# ==========================================================

@app.route("/marketplace")
def marketplace_page():
    return render_template("marketplace.html")

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


# ==========================================================
# MOMENTUM API
# ==========================================================
@app.route("/api/dashboard/momentum")
def api_momentum():
    labels = ["AI", "Jobs", "Skin", "MacBook"]
    values = [40, 23, 18, 10]
    return jsonify({"labels": labels, "values": values})


# ==========================================================
# INDEX + ROOM
# ==========================================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/room/<rid>")
def room_view(rid):
    return render_template("room.html", rid=rid)


# ==========================================================
# SERVER START
# ==========================================================
if __name__ == "__main__":
    print("=== CLEAN LOLA SERVER RUNNING ===")
    socketio.run(app, host="0.0.0.0", port=PORT)
''')

with open(path, "w") as f:
    f.writelines(clean)

print("✔ Bottom of app_full.py rebuilt cleanly.")
