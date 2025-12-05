import praw

reddit = praw.Reddit(
    client_id="qJyO9FoYahDuWnqG-JG5BA",
    client_secret="N2zF1Rj9HiIGDB2kfKxhmPO0m9A-gA",
    user_agent="TitleAnalyzer v1.0 (by /u/Unlucky-Ad7349)"
)

print("📝 REAL POST TITLES FROM REDDIT:")
print("=" * 40)

subreddits = ['relationships', 'personalfinance', 'productivity', 'careerguidance']

for sub in subreddits:
    print(f"\n--- r/{sub} ---")
    subreddit = reddit.subreddit(sub)
    for i, post in enumerate(subreddit.top(time_filter="week", limit=5)):
        print(f"{i+1}. {post.title}")
    
    if input("\nPress Enter for next subreddit (or 'q' to quit): ").lower() == 'q':
        break
