import argparse
from techdebtzero.metrics.debt_score import compute_debt_score, generate_report

def main():
    parser = argparse.ArgumentParser(description="TechDebtZero CLI")
    parser.add_argument("command", choices=["analyze", "score", "report"], help="Command to run")
    parser.add_argument("--path", default=".", help="Path to analyze")
    args = parser.parse_args()

    if args.command == "analyze":
        print(f"🔍 Deep analyzing {args.path} ...")
        generate_report(args.path)
    elif args.command == "score":
        score = compute_debt_score(args.path)
        print(f"🏗️ Technical Debt Score: {score}/100")
    elif args.command == "report":
        generate_report(args.path)

if __name__ == "__main__":
    main()
