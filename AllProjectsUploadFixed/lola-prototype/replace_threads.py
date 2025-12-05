import re

fn = "app_full.py"
with open(fn) as f:
    src = f.read()

# Convert threading.Thread(...).start() → gevent.spawn(func)
pattern = r'threading\.Thread\((.*?)\)\.start\(\)'
def repl(m):
    inner = m.group(1)
    tgt = re.search(r'target\s*=\s*([A-Za-z0-9_\.]+)', inner)
    if tgt:
        return f"gevent.spawn({tgt.group(1)})"
    return "gevent.spawn(lambda: None)"

src = re.sub(pattern, repl, src, flags=re.S)

# Remove standalone thread creation (best-effort):
src = src.replace("threading.Thread", "# threading removed → using gevent.spawn")

with open(fn, "w") as f:
    f.write(src)

print("✔ Threading replaced with gevent.spawn.")
