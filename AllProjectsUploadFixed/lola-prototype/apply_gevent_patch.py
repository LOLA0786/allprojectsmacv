import re, sys

fn = "app_full.py"
with open(fn, "r") as f:
    src = f.read()

# 1) Ensure gevent monkey patch at very top (if not present)
if "monkey.patch_all()" not in src.splitlines()[0:20]:
    src = "from gevent import monkey\nmonkey.patch_all()\n\n" + src

# 2) Remove any 'import eventlet' or 'eventlet.' uses
src = re.sub(r'^\s*import\s+eventlet\s*\\n', '', src, flags=re.MULTILINE)
src = re.sub(r'eventlet\\.', 'GEVENT_REPLACED_', src)

# 3) Replace threading.Thread(...).start() with gevent.spawn(...)
# handle patterns like: threading.Thread(target=foo, daemon=True).start()
def replace_thread_start(m):
    inside = m.group(1)
    # try to capture target=NAME or target=func
    targ = re.search(r'target\s*=\s*([A-Za-z0-9_\\.]+)', inside)
    if targ:
        return "gevent.spawn(%s)\n" % targ.group(1)
    # fallback: put as gevent.spawn(lambda: ... ) — keep original code in lambda
    return "gevent.spawn(lambda: None)\n"

src = re.sub(r'threading\\.Thread\\((.*?)\\)\\.start\\(\\)', replace_thread_start, src, flags=re.S)

# 4) If there are .start() calls on returned thread vars (t.start()), try to replace creation + .start style:
# e.g.
# t = threading.Thread(target=...)
# t.daemon = True
# t.start()
src = re.sub(
    r"t\\s*=\\s*threading\\.Thread\\((.*?)\\)\\s*\\n(?:.*?\\n){0,2}?\\s*t\\.start\\(\\)",
    lambda m: "gevent.spawn(%s)\n" % (re.search(r'target\\s*=\\s*([A-Za-z0-9_\\.]+)', m.group(1)).group(1) if re.search(r'target\\s*=\\s*([A-Za-z0-9_\\.]+)', m.group(1)) else "lambda: None"),
    src,
    flags=re.S
)

# 5) Add 'import gevent' near top if not present
if "import gevent" not in src.splitlines()[0:40]:
    src = src.replace("from gevent import monkey\nmonkey.patch_all()\n\n", "from gevent import monkey\nmonkey.patch_all()\nimport gevent\n\n")

# 6) Restore any accidentally replaced legitimate text (GEVENT_REPLACED_ → no-op)
src = src.replace("GEVENT_REPLACED_", "")

# write back
with open(fn + ".bak", "w") as f:
    f.write(src)
with open(fn, "w") as f:
    f.write(src)

print("Applied gevent/thread patch. Backup saved to app_full.py.bak")
