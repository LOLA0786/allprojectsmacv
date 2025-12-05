import praw
from collections import Counter
import re

print("🚀 SMART REDDIT PROBLEM FINDER")
print("=" * 45)

# Your credentials
reddit = praw.Reddit(
    client_id="qJyO9FoYahDuWnqG-JG5BA",
    client_secret="N2zF1Rj9HiIGDB2kfKxhmPO0m9A-gA",
    user_agent="SmartFinder v1.0 (by /u/Unlucky-Ad7349)"
)

print("🔍 Scanning Reddit for REAL problems...")

# Problem-focused subreddits
subreddits = [
    'personalfinance', 'productivity', 'relationships', 
    'mentalhealth', 'careerguidance', 'selfimprovement'
]

all_text = ""

for sub in subreddits:
    print(f"🔎 Scanning r/{sub}...")
    try:
        subreddit = reddit.subreddit(sub)
        for post in subreddit.top(time_filter="week", limit=25):
            # Focus on titles which usually state the problem clearly
            all_text += " " + post.title
    except Exception as e:
        print(f"   Skipped r/{sub}: {e}")
        continue

print(f"📝 Collected text from {len(all_text)} characters")

# Better text cleaning
words = all_text.lower().split()

# Remove punctuation and short words
words = [re.sub(r'[^a-z]', '', word) for word in words]
words = [word for word in words if len(word) > 4]  # Longer words are more meaningful

# Comprehensive stop words list
stop_words = {
    'this', 'that', 'with', 'have', 'from', 'they', 'what', 'when', 'were', 
    'your', 'been', 'more', 'also', 'like', 'just', 'about', 'dont', 'even',
    'because', 'know', 'then', 'said', 'some', 'would', 'could', 'should',
    'which', 'their', 'there', 'them', 'were', 'been', 'being', 'than',
    'other', 'these', 'those', 'while', 'might', 'every', 'where', 'much',
    'such', 'very', 'many', 'most', 'over', 'after', 'before', 'since',
    'until', 'upon', 'without', 'within', 'among', 'between', 'during'
}

words = [word for word in words if word not in stop_words]

# Count words
word_counts = Counter(words)

print("\n🏆 REAL PROBLEMS PEOPLE FACE:")
print("=" * 35)

top_words = word_counts.most_common(20)
for i, (word, count) in enumerate(top_words, 1):
    print(f"{i:2d}. {word:15} - {count} mentions")

print("\n💡 ACTUAL BUSINESS OPPORTUNITIES:")
print("=" * 40)

# Problem-to-solution mapping
problem_solutions = {
    'money': "💰 Smart budgeting app with automated savings",
    'time': "⏰ AI time management coach", 
    'work': "💼 Productivity toolkit for remote workers",
    'feel': "😊 Mental wellness tracker with coping strategies",
    'stress': "🧘 Stress management companion",
    'anxiety': "🌱 Anxiety relief exercises app",
    'relationship': "💑 Relationship communication helper",
    'financial': "📈 Personal finance advisor app",
    'career': "🚀 Career path discovery platform",
    'learning': "🎓 Personalized learning roadmap",
    'health': "❤️ Health habit builder",
    'sleep': "😴 Sleep quality optimizer",
    'focus': "🎯 Distraction blocker with analytics",
    'saving': "🏦 Automated savings assistant",
    'budget': "📊 Visual budget planner",
    'debt': "💳 Debt payoff strategist",
    'lonely': "👥 Social connection facilitator",
    'procrastination': "⚡ Procrastination breaker",
    'overwhelmed': "🌈 Overwhelm reducer toolkit",
    'stuck': "🔓 Unstuck yourself guide"
}

print("\n🎯 SOLUTIONS FOR TOP PROBLEMS:")
found_solutions = 0
for word, count in top_words:
    if word in problem_solutions and found_solutions < 8:
        print(f"• {problem_solutions[word]}")
        print(f"  (Solves '{word}' problems - mentioned {count} times)")
        print()
        found_solutions += 1

if found_solutions == 0:
    print("\n🤔 No clear problems found. Let's try a different approach...")
    print("Top words found:", [word for word, count in top_words[:10]])

print(f"\n✅ Found {found_solutions} clear business opportunities!")
