import praw
from collections import Counter
import re

print("🚀 SIMPLE REDDIT PROBLEM FINDER")
print("=" * 40)

# Your credentials
reddit = praw.Reddit(
    client_id="qJyO9FoYahDuWnqG-JG5BA",
    client_secret="N2zF1Rj9HiIGDB2kfKxhmPO0m9A-gA",
    user_agent="SimpleFinder v1.0 (by /u/Unlucky-Ad7349)"
)

print("🔍 Scanning Reddit for problems...")

# Simple subreddit list
subreddits = ['offmychest', 'personalfinance', 'productivity', 'relationships', 'work']

all_text = ""

for sub in subreddits:
    print(f"Checking r/{sub}...")
    try:
        subreddit = reddit.subreddit(sub)
        for post in subreddit.top(time_filter="week", limit=20):
            all_text += " " + post.title + " " + post.selftext
    except:
        continue

print(f"📝 Collected {len(all_text)} characters of text")

# Clean and analyze
words = all_text.lower().split()
words = [re.sub(r'[^a-z]', '', word) for word in words]
words = [word for word in words if len(word) > 3]

# Remove common words
common_words = {'this', 'that', 'with', 'have', 'from', 'they', 'what', 'when', 'were', 'your', 'been', 'more', 'also'}
words = [word for word in words if word not in common_words]

# Count words
word_counts = Counter(words)

print("\n🏆 TOP 15 PROBLEMS PEOPLE DISCUSS:")
print("=" * 35)

top_words = word_counts.most_common(15)
for i, (word, count) in enumerate(top_words, 1):
    print(f"{i:2d}. {word:12} - {count} mentions")

print("\n💡 BUSINESS IDEAS:")
print("=" * 20)

ideas = {
    'time': "⏰ Time management app",
    'work': "💼 Productivity tool", 
    'money': "💰 Financial helper",
    'feel': "😊 Mental wellness app",
    'people': "👥 Social connection tool",
    'help': "🆚 Support community platform",
    'like': "👍 Recommendation engine",
    'think': "🤔 Decision helper",
    'need': "🎯 Problem-solving app",
    'want': "🛒 Goal achievement tool"
}

for word, count in top_words[:8]:
    if word in ideas:
        print(f"• {ideas[word]} (because '{word}' mentioned {count} times)")
    else:
        print(f"• App to solve {word} problems ({count} mentions)")

print(f"\n✅ Analysis complete! Found {len(top_words)} common problems.")
