import re

path = "app_full.py"
txt = open(path).read()

# Remove all duplicate new UI blocks fully
txt = re.sub(
    r"# ==========================================================\n# NEW UI ROUTES[\s\S]*?# ==========================================================\n# Dashboard API for Momentum",
    "",
    txt,
    flags=re.MULTILINE
)

# Insert a single clean block
clean_block = '''
# ==========================================================
# NEW UI ROUTES — Marketplace, Product, Mentors, Premium, Dashboard v2
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
# Dashboard API for Momentum (used by D3 chart)
# ==========================================================
'''
# Insert just above the momentum API block
txt = re.sub(r"# ==========================================================\n# Dashboard API for Momentum", clean_block, txt)

open(path, "w").write(txt)
print("✔ Cleaned duplicate UI routes and restored a single block.")
