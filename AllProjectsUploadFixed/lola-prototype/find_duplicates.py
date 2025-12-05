import ast

path = "app_full.py"
tree = ast.parse(open(path).read())

funcs = {}
dupes = []

for node in tree.body:
    if isinstance(node, ast.FunctionDef):
        name = node.name
        if name in funcs:
            dupes.append((name, node.lineno))
        else:
            funcs[name] = node.lineno

print("\n=== DUPLICATE FUNCTIONS FOUND ===")
for name, ln in dupes:
    print(f"{name} at line {ln}")
if not dupes:
    print("No duplicates.")
