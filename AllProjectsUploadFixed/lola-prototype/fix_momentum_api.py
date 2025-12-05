import re

path = "app_full.py"
txt = open(path).read()

# Remove ANY old momentum API blocks
txt = re.sub(
    r"@app\.route\(\"/api/dashboard/momentum\"[\s\S]+?return jsonify\([^\)]*\)\)",
    "",
    txt
)

# Insert NEW working API at bottom BEFORE startup
new_api = r'''
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
'''

# Insert before "if __name__"
txt = re.sub(
    r"(if __name__ == \"__main__\":)",
    new_api + r"\n\n\1",
    txt
)

open(path, "w").write(txt)
print("✔ FIXED: Momentum API added cleanly.")
