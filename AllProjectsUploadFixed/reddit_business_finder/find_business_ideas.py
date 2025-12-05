import praw
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import datetime

print("🚀 REDDIT BUSINESS IDEA FINDER")
print("=" * 50)

# YOUR REDDIT CREDENTIALS
REDDIT_CREDENTIALS = {
    "client_id": "qJyO9FoYahDuWnqG-JG5BA",
    "client_secret": "N2zF1Rj9HiIGDB2kfKxhmPO0m9A-gA", 
    "user_agent": "BusinessIdeaFinder v1.0 (by /u/Unlucky-Ad7349)"
}

def setup_reddit():
    print("🔧 Connecting to Reddit...")
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CREDENTIALS["client_id"],
            client_secret=REDDIT_CREDENTIALS["client_secret"],
            user_agent=REDDIT_CREDENTIALS["user_agent"]
        )
        reddit.read_only = True
        # Test connection
        reddit.subreddit("all").hot(limit=1)
        print("✅ Connected to Reddit successfully!")
        return reddit
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

def scrape_reddit_posts(reddit):
    print("\n🎯 Scraping popular subreddits for problems...")
    
    subreddits = [
        'offmychest', 'self', 'relationships', 'personalfinance',
        'Advice', 'productivity', 'work', 'learnprogramming', 
        'smallbusiness', 'mentalhealth', 'careerguidance', 'lifehacks'
    ]
    
    all_posts = []
    
    for sub_name in subreddits:
        print(f"   Scanning r/{sub_name}...", end=" ")
        try:
            subreddit = reddit.subreddit(sub_name)
            post_count = 0
            
            # Get top posts from this month
            for post in subreddit.top(time_filter="month", limit=30):
                if not post.stickied and post.title:
                    # Get some comments
                    post.comments.replace_more(limit=0)
                    comments = ' '.join([comment.body for comment in post.comments.list()[:3]])
                    
                    all_posts.append({
                        'subreddit': sub_name,
                        'title': post.title,
                        'content': post.selftext,
                        'upvotes': post.score,
                        'comments': comments,
                        'url': f"https://reddit.com{post.permalink}"
                    })
                    post_count += 1
            
            print(f"✅ {post_count} posts")
            
        except Exception as e:
            print(f"❌ failed")
            continue
    
    return all_posts

def analyze_problems(posts_data):
    print("\n📊 Analyzing most common problems...")
    
    # Combine all text
    all_text = ""
    for post in posts_data:
        all_text += " " + post['title'] + " " + post['content'] + " " + post['comments']
    
    # Clean text
    all_text = all_text.lower()
    all_text = re.sub(r'[^a-zA-Z\s]', ' ', all_text)
    all_text = re.sub(r'\s+', ' ', all_text)
    
    # Common words to ignore
    stop_words = {
        'the', 'and', 'you', 'that', 'for', 'with', 'have', 'this', 'but', 'not',
        'are', 'from', 'can', 'your', 'was', 'what', 'how', 'will', 'one', 'should',
        'because', 'when', 'who', 'where', 'which', 'their', 'been', 'has', 'would',
        'there', 'more', 'like', 'just', 'some', 'than', 'then', 'also', 'very',
        'into', 'only', 'could', 'them', 'other', 'these', 'were', 'about', 'get',
        'being', 'make', 'people', 'through', 'first', 'most', 'over', 'after',
        'even', 'much', 'such', 'many', 'those', 'well', 'might', 'since', 'both'
    }
    
    # Count words
    words = all_text.split()
    word_counts = Counter(words)
    
    # Filter meaningful words
    problem_words = {}
    for word, count in word_counts.items():
        if (len(word) > 3 and 
            word not in stop_words and 
            count > 5 and
            not word.isdigit()):
            problem_words[word] = count
    
    return problem_words

def suggest_business_ideas(top_problems):
    print("\n💡 BUSINESS OPPORTUNITIES FOUND:")
    print("=" * 50)
    
    top_20 = Counter(top_problems).most_common(20)
    
    print("\n🏆 TOP PROBLEMS PEOPLE FACE:")
    for i, (problem, count) in enumerate(top_20, 1):
        print(f"{i:2d}. {problem:15} (mentioned {count} times)")
    
    # Business ideas based on common problems
    print("\n🚀 POTENTIAL BUSINESS IDEAS:")
    ideas = []
    
    problem_categories = {
        'time': "Time management app with AI scheduling assistant",
        'work': "Remote work productivity toolkit with focus features", 
        'money': "Simple financial planning app for beginners",
        'learn': "Personalized learning platform with AI tutor",
        'focus': "Distraction-blocking app with productivity analytics",
        'stress': "Mental wellness app with daily coping exercises",
        'sleep': "Smart sleep tracker with improvement recommendations",
        'health': "Personal health assistant with habit tracking",
        'social': "Social connection app for meaningful relationships",
        'code': "AI programming assistant for beginners and pros",
        'business': "Startup toolkit with step-by-step guidance",
        'career': "Career path finder with skill assessment",
        'relationship': "Communication helper for better relationships",
        'budget': "Automated budget tracker with savings goals",
        'exercise': "Personalized workout planner for home exercises"
    }
    
    for problem, count in top_20[:10]:
        if problem in problem_categories:
            ideas.append(problem_categories[problem])
        else:
            ideas.append(f"App to help with {problem} problems")
    
    for i, idea in enumerate(ideas[:8], 1):
        print(f"{i}. {idea}")

def create_visualizations(top_problems, posts_data):
    print("\n📈 Creating visualizations...")
    
    # Create results folder
    os.makedirs('results', exist_ok=True)
    
    # Top 15 problems chart
    top_15 = Counter(top_problems).most_common(15)
    problems, counts = zip(*top_15)
    
    plt.figure(figsize=(12, 8))
    bars = plt.barh(problems, counts, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
    plt.xlabel('How Often Mentioned')
    plt.title('Top 15 Problems People Discuss on Reddit')
    plt.gca().invert_yaxis()
    
    # Add counts to bars
    for bar, count in zip(bars, counts):
        plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                f'{count}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('results/top_problems.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Word cloud
    wordcloud = WordCloud(width=1200, height=600, 
                         background_color='white',
                         max_words=50).generate_from_frequencies(top_problems)
    
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Common Problem Words')
    plt.tight_layout()
    plt.savefig('results/problems_wordcloud.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Visualizations saved to 'results/' folder")

def main():
    print("🎯 Mission: Find the most common problems to build businesses around!")
    print(f"⏰ Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Connect to Reddit
    reddit = setup_reddit()
    if not reddit:
        return
    
    # Scrape data
    posts = scrape_reddit_posts(reddit)
    
    if not posts:
        print("❌ No data collected. Check your Reddit credentials.")
        return
    
    print(f"\n✅ Collected {len(posts)} posts from Reddit!")
    
    # Analyze problems
    problems = analyze_problems(posts)
    
    # Save raw data
    df = pd.DataFrame(posts)
    df.to_csv('results/reddit_posts_data.csv', index=False)
    print("💾 Raw data saved to 'results/reddit_posts_data.csv'")
    
    # Generate insights
    suggest_business_ideas(problems)
    create_visualizations(problems, posts)
    
    print(f"\n🎉 MISSION COMPLETE!")
    print("=" * 50)
    print("📁 Check the 'results' folder for:")
    print("   📊 top_problems.png - Chart of most common problems")
    print("   ☁️  problems_wordcloud.png - Visual word cloud") 
    print("   📄 reddit_posts_data.csv - All collected posts")
    print(f"\n💡 Next: Pick a problem and let's build the solution!")

if __name__ == "__main__":
    main()
