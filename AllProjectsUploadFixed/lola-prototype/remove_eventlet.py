import re

fn = "app_full.py"
with open(fn) as f:
    src = f.read()

# Remove all import eventlet lines
src = re.sub(r'^\s*import\s+eventlet.*$', '', src, flags=re.MULTILINE)
src = re.sub(r'eventlet\.[A-Za-z0-9_]+', '', src)

# Remove stray eventlet warnings or comments
src = src.replace("Eventlet is deprecated", "")
src = src.replace("eventlet", "")

with open(fn, "w") as f:
    f.write(src)

print("✔ All eventlet references removed.")
