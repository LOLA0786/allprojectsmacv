path = "app_full.py"
txt = open(path).read().rstrip()

# Remove ANY existing broken bottom
import re
txt = re.sub(
    r"# ==========================================================\n# SERVER START[\s\S]*",
    "",
    txt,
    flags=re.MULTILINE
)

# Append clean server start
clean_block = '''

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

with open(path, "w") as f:
    f.write(txt + clean_block + "\n")

print("✔ Fixed server start block.")
