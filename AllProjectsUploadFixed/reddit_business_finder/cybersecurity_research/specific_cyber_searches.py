import praw

print("🔍 SPECIFIC CYBERSECURITY SEARCHES")
print("=" * 50)

reddit = praw.Reddit(
    client_id="qJyO9FoYahDuWnqG-JG5BA",
    client_secret="N2zF1Rj9HiIGDB2kfKxhmPO0m9A-gA",
    user_agent="SpecificCyber_Search v1.0 (by /u/Unlucky-Ad7349)"
)

# Search for specific cybersecurity incidents
searches = [
    "data breach",
    "ransomware attack", 
    "phishing campaign",
    "zero-day vulnerability",
    "malware outbreak",
    "privacy violation",
    "hack",
    "security incident"
]

print("🎯 Searching for specific cybersecurity incidents...\n")

for search_term in searches:
    print(f"🔎 '{search_term}':")
    try:
        for post in reddit.subreddit("all").search(search_term, limit=5):
            # Only show from relevant subreddits
            if any(sub in post.subreddit.display_name.lower() for sub in ['cyber', 'security', 'privacy', 'hack', 'tech']):
                print(f"   📝 {post.title[:80]}...")
                print(f"      r/{post.subreddit} | 👍 {post.score} | 💬 {post.num_comments}")
                print(f"      🔗 https://reddit.com{post.permalink}")
                print()
    except Exception as e:
        print(f"   ❌ Search failed: {e}")
        continue

print("💡 Look for patterns in these search results!")
