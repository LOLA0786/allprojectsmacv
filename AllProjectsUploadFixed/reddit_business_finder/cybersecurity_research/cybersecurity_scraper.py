import praw
from collections import Counter
import pandas as pd
import re

print("🔐 GLOBAL CYBERSECURITY PROBLEM SCRAPER")
print("=" * 55)

reddit = praw.Reddit(
    client_id="qJyO9FoYahDuWnqG-JG5BA",
    client_secret="N2zF1Rj9HiIGDB2kfKxhmPO0m9A-gA",
    user_agent="Cybersecurity_Research v1.0 (by /u/Unlucky-Ad7349)"
)

# Cybersecurity-focused subreddits
cybersecurity_subreddits = [
    'cybersecurity', 'netsec', 'asknetsec', 'malware', 
    'reverseengineering', 'computerforensics', 'networking',
    'privacy', 'hacking', 'HowToHack', 'blackhat',
    'redteamsec', 'blueteamsec', 'bugbounty',
    'security', 'informationsecurity', 'databreaches',
    'crypto', 'VPN', 'tor', 'opsec'
]

# Cybersecurity problem categories
cyber_problems = {
    'data_breaches': ['data breach', 'hacked', 'compromised', 'leaked data', 'data theft'],
    'ransomware': ['ransomware', 'encrypted files', 'bitcoin payment', 'decryptor'],
    'phishing': ['phishing', 'fake email', 'credential theft', 'social engineering'],
    'malware': ['malware', 'virus', 'trojan', 'infected', 'antivirus'],
    'vulnerabilities': ['vulnerability', 'zero-day', 'exploit', 'patch', 'update'],
    'privacy': ['privacy', 'tracking', 'surveillance', 'data collection'],
    'compliance': ['compliance', 'gdpr', 'hipaa', 'regulation', 'audit'],
    'cloud_security': ['cloud security', 'aws security', 'azure security', 'cloud breach'],
    'iot_security': ['iot security', 'smart device', 'camera hacked', 'iot vulnerability'],
    'supply_chain': ['supply chain', 'third-party risk', 'vendor security'],
    'ai_security': ['ai security', 'ml security', 'ai vulnerability', 'model poisoning'],
    'cryptocurrency': ['crypto hack', 'wallet hacked', 'exchange breach', 'defi hack']
}

print("🔍 Scanning global cybersecurity communities for problems...")

cyber_posts_data = []
problem_mentions = Counter()
industry_mentions = Counter()

# Industry sectors for analysis
industries = {
    'healthcare': ['hospital', 'medical', 'healthcare', 'patient data', 'hipaa'],
    'finance': ['bank', 'financial', 'payment', 'credit card', 'fintech'],
    'government': ['government', 'federal', 'state', 'military', 'defense'],
    'education': ['school', 'university', 'student', 'education'],
    'retail': ['retail', 'ecommerce', 'pos', 'payment system'],
    'energy': ['energy', 'utility', 'power grid', 'scada'],
    'manufacturing': ['manufacturing', 'factory', 'industrial', 'ics']
}

for sub_name in cybersecurity_subreddits:
    print(f"   Scanning r/{sub_name}...", end=" ")
    try:
        subreddit = reddit.subreddit(sub_name)
        post_count = 0
        
        # Get recent cybersecurity problem discussions
        for post in subreddit.top(time_filter="month", limit=60):
            title_lower = post.title.lower()
            content_lower = post.selftext.lower()
            full_text = title_lower + " " + content_lower
            
            # Check if post discusses security problems
            has_security_issue = any(
                keyword in full_text 
                for keyword in ['problem', 'issue', 'vulnerability', 'breach', 
                              'hack', 'attack', 'compromise', 'threat',
                              'risk', 'exploit', 'malware', 'ransomware']
            )
            
            if has_security_issue:
                # Track cybersecurity problem categories
                for category, keywords in cyber_problems.items():
                    if any(keyword in full_text for keyword in keywords):
                        problem_mentions[category] += 1
                
                # Track industries affected
                for industry, keywords in industries.items():
                    if any(keyword in full_text for keyword in keywords):
                        industry_mentions[industry] += 1
                
                # Store post data
                post_data = {
                    'subreddit': sub_name,
                    'title': post.title,
                    'content': post.selftext[:500],
                    'upvotes': post.score,
                    'comments': post.num_comments,
                    'url': f"https://reddit.com{post.permalink}",
                    'problem_categories': [],
                    'industries_mentioned': [],
                    'severity_level': 'medium'  # default
                }
                
                # Add specific problem categories
                for category, keywords in cyber_problems.items():
                    if any(keyword in full_text for keyword in keywords):
                        post_data['problem_categories'].append(category)
                
                # Add industries mentioned
                for industry, keywords in industries.items():
                    if any(keyword in full_text for keyword in keywords):
                        post_data['industries_mentioned'].append(industry)
                
                # Determine severity
                if any(word in full_text for word in ['critical', 'emergency', 'urgent', 'major breach']):
                    post_data['severity_level'] = 'critical'
                elif any(word in full_text for word in ['high risk', 'serious', 'exploited']):
                    post_data['severity_level'] = 'high'
                
                cyber_posts_data.append(post_data)
                post_count += 1
        
        print(f"✅ {post_count} security issues")
        
    except Exception as e:
        print(f"❌ skipped: {e}")
        continue

print(f"\n📊 Collected {len(cyber_posts_data)} cybersecurity problem discussions")

# Analyze results
print("\n🏆 TOP CYBERSECURITY THREATS:")
print("=" * 45)

for problem, count in problem_mentions.most_common(15):
    print(f"   {problem:25} - {count} mentions")

print("\n🏢 MOST AFFECTED INDUSTRIES:")
print("=" * 35)
for industry, count in industry_mentions.most_common(10):
    print(f"   {industry:20} - {count} mentions")

print("\n💡 CYBERSECURITY BUSINESS OPPORTUNITIES:")
print("=" * 50)

# Cybersecurity business ideas
cyber_business_ideas = {
    'data_breaches': "🛡️ Automated Data Breach Detection & Response Platform",
    'ransomware': "🔒 Ransomware Protection & Recovery Solution",
    'phishing': "🎣 AI-Powered Phishing Detection & Employee Training",
    'malware': "🦠 Next-Gen Malware Analysis & Protection",
    'vulnerabilities': "🔍 Automated Vulnerability Management Platform",
    'privacy': "👁️ Privacy Compliance & Data Protection Tools",
    'compliance': "📊 Automated Compliance Management for GDPR/HIPAA",
    'cloud_security': "☁️ Cloud Security Posture Management",
    'iot_security': "📱 IoT Device Security & Monitoring",
    'supply_chain': "⛓️ Third-Party Risk Management Platform",
    'ai_security': "🤖 AI Model Security & Adversarial Protection",
    'cryptocurrency': "₿ Crypto Wallet Security & Exchange Protection"
}

print("\n🎯 VALIDATED CYBERSECURITY STARTUP IDEAS:")
validated_count = 0
for problem, count in problem_mentions.most_common(12):
    if problem in cyber_business_ideas and count >= 3:
        print(f"• {cyber_business_ideas[problem]}")
        print(f"  📊 Market Need: '{problem}' mentioned {count} times")
        print()
        validated_count += 1

# Show top cybersecurity problem posts
print("\n🔥 TOP CYBERSECURITY PROBLEMS:")
print("=" * 45)

if cyber_posts_data:
    top_posts = sorted(cyber_posts_data, key=lambda x: x['upvotes'], reverse=True)[:15]
    
    for i, post in enumerate(top_posts, 1):
        print(f"\n{i}. {post['title']}")
        print(f"   🔗 r/{post['subreddit']} | 👍 {post['upvotes']} | 💬 {post['comments']} comments")
        print(f"   🚨 Severity: {post['severity_level'].upper()}")
        if post['problem_categories']:
            print(f"   🎯 Threats: {', '.join(post['problem_categories'][:3])}")
        if post['industries_mentioned']:
            print(f"   🏢 Industries: {', '.join(post['industries_mentioned'])}")
        print(f"   📎 {post['url']}")
else:
    print("No cybersecurity problems found. Let's search differently...")

# Save detailed analysis
import os
os.makedirs('cyber_analysis', exist_ok=True)

if cyber_posts_data:
    df = pd.DataFrame(cyber_posts_data)
    df.to_csv('cyber_analysis/cybersecurity_problems.csv', index=False)
    print(f"\n📁 Analysis saved to 'cyber_analysis/' folder")

print(f"\n✅ Found {validated_count} validated cybersecurity business opportunities!")
print("💡 Build solutions that address the most critical global security threats!")
