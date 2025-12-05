path = "app_full.py"

# Read full file
with open(path) as f:
    lines = f.readlines()

# Keep only the top safe part (first ~120 lines)
clean_top = lines[:120]

clean_bottom = '''

# ==========================================================
# UI ROUTES — Marketplace / Product / Mentors / Premium / Dashboard v2
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
    return jsonify({
        "labels": ["AI", "Jobs", "Skin", "MacBook"],
        "values": [40, 22, 18, 12]
    })


# ==========================================================
# MAIN PAGES
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
    socketio.run(
        app,
        host="0.0.0.0",
        port=PORT,
        debug=False
    )
'''

# Write final file
with open(path, "w") as f:
    f.writelines(clean_top)
    f.write(clean_bottom)

print("✔ Entire bottom of app_full.py rebuilt CLEAN.")
