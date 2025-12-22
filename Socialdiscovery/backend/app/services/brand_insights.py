from collections import Counter
from app.models.moment import Moment

def trending_topics(db, limit=5):
    moments = db.query(Moment).all()
    topics = [m.intent for m in moments]
    return Counter(topics).most_common(limit)

def trending_words(db, limit=10):
    moments = db.query(Moment).all()
    words = []
    for m in moments:
        words.extend(m.intent.split())

    return Counter(words).most_common(limit)

def ai_topics(db):
    moments = db.query(Moment).all()
    themes = {}

    for m in moments:
        if "battery" in m.intent:
            themes.setdefault("Device Reliability", 0)
            themes["Device Reliability"] += 1
        if "startup" in m.intent:
            themes.setdefault("Startup Anxiety", 0)
            themes["Startup Anxiety"] += 1
        if "ai" in m.intent:
            themes.setdefault("AI Adoption", 0)
            themes["AI Adoption"] += 1

    return themes

def trending_ideas(db):
    return [
        "Offer battery replacement subscriptions for travelers",
        "Target founders worried about runway and funding",
        "Market AI tools as productivity stress-reducers"
    ]
