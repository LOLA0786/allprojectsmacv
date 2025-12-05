import re

path = "app_full.py"
txt = open(path).read()

# Delete any OLD endpoint definitions above line ~140
pattern = r"""
@app\.route.*?\)     # route decorator
\s*def\s+(index|room_view|marketplace_page|product_detail|mentors_page|premium_page|dashboard_v2_page)\s*\(.*?
(?:\n\s+.*?)*?\n\n
"""

clean = re.sub(pattern, "", txt, flags=re.MULTILINE | re.DOTALL | re.VERBOSE)

open(path, "w").write(clean)
print("✔ Removed all OLD route functions above line 140")
