import re

path = "app_full.py"
txt = open(path).read()

# Delete everything from @app.route("/marketplace") until before DEBUG or next section
txt = re.sub(
    r"@app\.route\(\"/marketplace\"[\s\S]+?def dashboard_v2_page.*?\n",
    "",
    txt
)

# Insert clean block
clean_block = '''
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
'''

# Insert this block AFTER the dashboard_view definition
txt = re.sub(
    r"def dashboard_view[\s\S]+?return render_template\(\"dashboard\.html\"\)\n",
    r"\g<0>\n" + clean_block + "\n",
    txt
)

open(path, "w").write(txt)
print("✔ UI routes fully rebuilt and duplicates removed")
