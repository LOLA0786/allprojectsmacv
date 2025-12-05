import os
import subprocess
from radon.complexity import cc_visit
from radon.metrics import mi_visit

def compute_radon_metrics(path="."):
    """Compute average cyclomatic complexity and maintainability index."""
    complexities = []
    maintainability = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(".py"):
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, "r", encoding="utf-8") as code_file:
                        code = code_file.read()
                    # Cyclomatic complexity
                    results = cc_visit(code)
                    if results:
                        complexities.extend([r.complexity for r in results])
                    # Maintainability Index
                    maintainability.append(mi_visit(code, True))
                except Exception:
                    pass

    avg_complexity = round(sum(complexities) / len(complexities), 2) if complexities else 0
    avg_mi = round(sum(maintainability) / len(maintainability), 2) if maintainability else 100
    return avg_complexity, avg_mi


def compute_pylint_score(path="."):
    """Run pylint and extract the global evaluation score."""
    try:
        result = subprocess.run(
            ["pylint", "--disable=R,C", path],
            capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if "Your code has been rated at" in line:
                score = float(line.split("at")[-1].split("/")[0].strip())
                return score
    except Exception:
        pass
    return 10.0


def count_todos(path="."):
    """Count TODO and FIXME comments."""
    count = 0
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(".py"):
                try:
                    with open(os.path.join(root, f), "r", encoding="utf-8") as fh:
                        content = fh.read()
                    count += content.count("TODO") + content.count("FIXME")
                except Exception:
                    pass
    return count


def compute_debt_score(path="."):
    """Combine multiple metrics into a final 0–100 score."""
    complexity, mi = compute_radon_metrics(path)
    pylint_score = compute_pylint_score(path)
    todos = count_todos(path)

    score = (
        (100 - (complexity * 1.5)) * 0.3 +
        mi * 0.3 +
        pylint_score * 5 * 0.3 +
        max(0, 100 - (todos * 0.5)) * 0.1
    )
    return round(max(0, min(score, 100)), 2)


def generate_report(path=".", output="reports/debt_report.md"):
    """Generate a Markdown report summarizing all metrics."""
    os.makedirs(os.path.dirname(output), exist_ok=True)
    complexity, mi = compute_radon_metrics(path)
    pylint_score = compute_pylint_score(path)
    todos = count_todos(path)
    final_score = compute_debt_score(path)

    with open(output, "w", encoding="utf-8") as f:
        f.write(f"# 🧠 TechDebtZero Report\n\n")
        f.write(f"**Path:** `{path}`\n\n")
        f.write(f"## 📊 Metrics\n")
        f.write(f"- Average Cyclomatic Complexity: `{complexity}`\n")
        f.write(f"- Average Maintainability Index: `{mi}`\n")
        f.write(f"- Pylint Score: `{pylint_score}/10`\n")
        f.write(f"- TODO/FIXME Count: `{todos}`\n\n")
        f.write(f"## 🏗️ Final Technical Debt Score: **{final_score}/100**\n")

    print(f"✅ Report generated at: {output}")
