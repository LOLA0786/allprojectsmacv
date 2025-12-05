import praw
from collections import Counter
import pandas as pd
import datetime

print("🔐 WORKING CYBERSECURITY PROBLEM SCRAPER")
print("=" * 55)

reddit = praw.Reddit(
    client_id="qJyO9FoYahDuWnqG-JG5BA",
    client_secret="N2zF1Rj9HiIGDB2kfKxhmPO0m9A-gA",
    user_agent="WorkingCyber_Scraper v1.0 (by /u/Unlucky-Ad7349)"
)

print("🔍 Scanning cybersecurity communities for REAL problems...")

# Get actual posts from cybersecurity subreddits
cyber_subreddits = ['cybersecurity', 'privacy', 'netsec', 'hacking', 'malware']

all_posts = []
problem_categories = Counter()

for sub_name in cyber_subreddits:
    print(f"📡 Scanning r/{sub_name}...")
    try:
        subreddit = reddit.subreddit(sub_name)
        
        # Get HOT posts (current discussions)
        for post in subreddit.hot(limit=50):
            title_lower = post.title.lower()
            
            # Check if this is about security problems
            is_problem_post = any(keyword in title_lower for keyword in [
                'breach', 'hack', 'attack', 'vulnerability', 'exploit',
                'malware', 'ransomware', 'phishing', 'leak', 'compromise',
                'security issue', 'data loss', 'privacy', 'surveillance',
                'zero-day', 'threat', 'risk'
            ])
            
            if is_problem_post:
                post_data = {
                    'subreddit': sub_name,
                    'title': post.title,
                    'content': post.selftext[:300] if post.selftext else '',
                    'upvotes': post.score,
                    'comments': post.num_comments,
                    'url': f"https://reddit.com{post.permalink}",
                    'created_utc': post.created_utc,
                    'problem_type': 'general',
                    'severity': 'medium'
                }
                
                # Categorize the problem
                if any(word in title_lower for word in ['breach', 'leak', 'data exposed']):
                    post_data['problem_type'] = 'data_breach'
                    problem_categories['data_breach'] += 1
                elif any(word in title_lower for word in ['ransomware', 'encrypted', 'bitcoin']):
                    post_data['problem_type'] = 'ransomware'
                    problem_categories['ransomware'] += 1
                elif any(word in title_lower for word in ['phishing', 'social engineering']):
                    post_data['problem_type'] = 'phishing'
                    problem_categories['phishing'] += 1
                elif any(word in title_lower for word in ['malware', 'virus', 'trojan']):
                    post_data['problem_type'] = 'malware'
                    problem_categories['malware'] += 1
                elif any(word in title_lower for word in ['vulnerability', 'zero-day', 'exploit']):
                    post_data['problem_type'] = 'vulnerabilities'
                    problem_categories['vulnerabilities'] += 1
                elif any(word in title_lower for word in ['privacy', 'surveillance', 'tracking']):
                    post_data['problem_type'] = 'privacy'
                    problem_categories['privacy'] += 1
                
                # Determine severity
                if any(word in title_lower for word in ['critical', 'major', 'emergency', 'massive']):
                    post_data['severity'] = 'critical'
                elif any(word in title_lower for word in ['serious', 'urgent', 'important']):
                    post_data['severity'] = 'high'
                
                all_posts.append(post_data)
                print(f"   ✅ Found: {post.title[:70]}...")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        continue

print(f"\n📊 Found {len(all_posts)} cybersecurity problem discussions")

# Show results
print("\n🏆 CYBERSECURITY PROBLEM CATEGORIES:")
print("=" * 45)
for category, count in problem_categories.most_common():
    print(f"   {category:20} - {count} posts")

print(f"\n🔥 TOP CYBERSECURITY PROBLEMS RIGHT NOW:")
print("=" * 50)

if all_posts:
    # Sort by upvotes and show top 20
    top_posts = sorted(all_posts, key=lambda x: x['upvotes'], reverse=True)[:20]
    
    for i, post in enumerate(top_posts, 1):
        print(f"\n{i}. {post['title']}")
        print(f"   🔗 r/{post['subreddit']} | 👍 {post['upvotes']} | 💬 {post['comments']} comments")
        print(f"   🚨 {post['problem_type'].upper()} | Severity: {post['severity'].upper()}")
        if post['content']:
            print(f"   📝 {post['content'][:100]}...")
        print(f"   📎 {post['url']}")
        
else:
    print("No posts found. Let me try a different approach...")
    
    # Alternative: Get top posts from all time
    print("\n🔄 TRYING ALTERNATIVE APPROACH: Top posts of all time")
    for sub_name in cyber_subreddits:
        try:
            subreddit = reddit.subreddit(sub_name)
            for post in subreddit.top(limit=10):
                print(f"   📈 r/{sub_name}: {post.title[:80]}... (👍 {post.score})")
        except:
            continue

# Save the data
import os
os.makedirs('cyber_results', exist_ok=True)

if all_posts:
    df = pd.DataFrame(all_posts)
    df.to_csv('cyber_results/cybersecurity_problems.csv', index=False)
    print(f"\n💾 Saved {len(all_posts)} problems to 'cyber_results/cybersecurity_problems.csv'")

# Business opportunity analysis
print(f"\n💡 CYBERSECURITY BUSINESS OPPORTUNITIES:")
print("=" * 50)

business_ideas = {
    'data_breach': "🛡️ BreachShield - Automated data breach detection and response",
    'ransomware': "🔒 RansomGuard - Ransomware protection and recovery platform", 
    'phishing': "🎣 PhishProof - AI-powered phishing detection and training",
    'malware': "🦠 MalwareDefender - Next-gen malware protection",
    'vulnerabilities': "🔍 VulnScanner - Automated vulnerability management",
    'privacy': "👁️ PrivacyGuard - Personal and corporate privacy protection"
}

print("\n🎯 VALIDATED BUSINESS IDEAS:")
for problem_type, count in problem_categories.most_common():
    if problem_type in business_ideas and count > 0:
        print(f"• {business_ideas[problem_type]}")
        print(f"  📊 Based on {count} {problem_type} problems found")
        print()

print(f"\n✅ Analysis complete! Found {sum(problem_categories.values())} total cybersecurity problems.")
