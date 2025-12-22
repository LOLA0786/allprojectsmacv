from collections import Counter

def summarize(intents: list[str]) -> str:
    if not intents:
        return "No active discussion yet."

    top = Counter(intents).most_common(1)[0][0]
    return f"People are actively discussing {top}. Interest is rising in real time."
