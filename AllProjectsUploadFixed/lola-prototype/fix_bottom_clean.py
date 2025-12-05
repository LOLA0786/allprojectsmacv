import re

path = "app_full.py"
txt = open(path).read()

# Remove all eventlet/gevent server code
txt = re.sub(
    r"if __name__ == ['\"]__main__['\"][\s\S]*?$",
    "",
    txt,
    flags=re.MULTILINE
)

clean_block = '''
# ==========================================================
# CLEAN & STABLE SERVER STARTUP (Werkzeug)
# ==========================================================
if __name__ == "__main__":
    print("\\n=== STARTING LOLA CLEAN SERVER ===")
    print("RUNNING FILE:", __file__)
    print("PORT:", PORT)
    print("===================================\\n")

    socketio.run(
        app,
        host="0.0.0.0",
        port=PORT,
        debug=True,
        use_reloader=False,
        allow_unsafe_werkzeug=True
    )
'''

txt += clean_block

open(path, "w").write(txt)
print("✔ Clean startup block restored")
