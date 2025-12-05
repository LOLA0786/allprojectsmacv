import io, os

path = "app_full.py"
start = 169
end = 210   # safe end (we stop after dashboard_v2_page)

with open(path) as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines, start=1):
    if start <= i <= end:
        continue
    new_lines.append(line)

with open(path, "w") as f:
    f.writelines(new_lines)

print("✔ Removed duplicate UI route block (lines 169–210)")
