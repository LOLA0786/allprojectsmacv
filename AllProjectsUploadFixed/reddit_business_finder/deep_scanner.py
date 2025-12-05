import praw
from collections import Counter
import re

print("🚀 DEEP REDDIT PROBLEM SCANNER")
print("=" * 45)

# Your credentials
reddit = praw.Reddit(
    client_id="qJyO9FoYahDuWnqG-JG5BA",
    client_secret="N2zF1Rj9HiIGDB2kfKxhmPO0m9A-gA",
    user_agent="DeepScanner v1.0 (by /u/Unlucky-Ad7349)"
)

print("🔍 DEEP Scanning Reddit for problems...")

# Expanded subreddit list focused on different problem areas
subreddits = [
    # Relationships & Social
    'relationships', 'relationship_advice', 'dating', 'marriage',
    # Money & Career
    'personalfinance', 'careerguidance', 'jobs', 'financialindependence',
    # Productivity & Work
    'productivity', 'getdisciplined', 'work', 'remotework',
    # Mental Health
    'anxiety', 'depression', 'mentalhealth', 'socialskills',
    # Life Problems
    'selfimprovement', 'lifeadvice', 'adulting', 'socialskills'
]

all_titles = ""
problem_keywords = set()

# Problem keywords we're looking for
target_problems = {
    'money', 'time', 'work', 'stress', 'anxiety', 'focus', 'lonely',
    'relationship', 'communication', 'financial', 'career', 'job',
    'productive', 'procrastination', 'overwhelmed', 'budget', 'debt',
    'saving', 'sleep', 'health', 'exercise', 'diet', 'friends',
    'family', 'parents', 'dating', 'marriage', 'breakup', 'divorce',
    'learning', 'study', 'skills', 'coding', 'programming', 'business',
    'startup', 'entrepreneur', 'social', 'confidence', 'shy'
}

for sub in subreddits:
    print(f"🔎 Scanning r/{sub}...")
    try:
        subreddit = reddit.subreddit(sub)
        # Get posts from different time frames
        for post in subreddit.top(time_filter="month", limit=30):
            title_lower = post.title.lower()
            all_titles += " " + title_lower
            
            # Check if title contains problem keywords
            for problem in target_problems:
                if problem in title_lower:
                    problem_keywords.add(problem)
                    
    except Exception as e:
        continue

print(f"📊 Scanned {len(subreddits)} subreddits")
print(f"🎯 Found {len(problem_keywords)} different problem types")

# Analyze the titles for common patterns
words = all_titles.split()

# Filter for meaningful words (longer than 4 chars)
words = [re.sub(r'[^a-z]', '', word) for word in words]
words = [word for word in words if len(word) > 4]

# Extended stop words
stop_words = {
    'about', 'after', 'again', 'against', 'although', 'always', 'because',
    'before', 'between', 'during', 'every', 'having', 'however', 'maybe',
    'might', 'never', 'nothing', 'often', 'other', 'really', 'since',
    'something', 'sometimes', 'still', 'their', 'there', 'these', 'thing',
    'think', 'those', 'through', 'together', 'until', 'usually', 'whatever',
    'when', 'where', 'while', 'would', 'years', 'could', 'should', 'which'
}

words = [word for word in words if word not in stop_words]

word_counts = Counter(words)

print("\n🏆 TOP PROBLEM AREAS IDENTIFIED:")
print("=" * 40)

# Show top problem-related words
top_problems = []
for word, count in word_counts.most_common(30):
    if count > 3:  # Only show words mentioned multiple times
        top_problems.append((word, count))

for i, (word, count) in enumerate(top_problems[:15], 1):
    print(f"{i:2d}. {word:18} - {count} mentions")

print("\n💡 BUSINESS OPPORTUNITIES ANALYSIS:")
print("=" * 45)

# Business ideas based on found problems
business_ideas = {
    'relationship': "💑 AI Relationship Coach - Helps with communication and conflict resolution",
    'anxiety': "😌 Anxiety Helper - Daily exercises and coping strategies", 
    'money': "💰 Financial Peace App - Simple budgeting and debt management",
    'time': "⏰ Time Optimizer - AI-powered schedule and focus management",
    'work': "💼 Productivity Pro - Distraction blocking and task management",
    'lonely': "👥 Social Connector - Helps build meaningful friendships",
    'career': "🚀 Career Navigator - Personalized career path guidance",
    'learning': "🎓 Skill Builder - AI learning paths for any skill",
    'stress': "🧘 Stress Reducer - Personalized stress management toolkit",
    'financial': "📈 Money Mentor - Automated financial advice for beginners"
}

print("\n🎯 VALIDATED BUSINESS IDEAS:")
validated_count = 0
for problem, count in top_problems:
    if problem in business_ideas and count > 5:
        print(f"• {business_ideas[problem]}")
        print(f"  📊 Validation: '{problem}' mentioned {count} times")
        print()
        validated_count += 1

if validated_count == 0:
    print("🤔 Let's look at the raw data to find patterns...")
    print("\n🔍 Most common words found:")
    for word, count in top_problems[:10]:
        print(f"   '{word}': {count} mentions")
    
    print("\n💡 Even without clear keywords, we can see what people are talking about!")
    print("   The most mentioned topics indicate where the pain points are.")

print(f"\n✅ Analysis complete! Found {validated_count} validated business opportunities.")
