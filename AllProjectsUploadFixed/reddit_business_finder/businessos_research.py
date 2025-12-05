import praw
from collections import Counter
import re

print("🚀 BusinessOS Deep Research Scraper")
print("=" * 50)

reddit = praw.Reddit(
    client_id="qJyO9FoYahDuWnqG-JG5BA",
    client_secret="N2zF1Rj9HiIGDB2kfKxhmPO0m9A-gA",
    user_agent="BusinessOS_Research v1.0 (by /u/Unlucky-Ad7349)"
)

# Target subreddits for deeper insights
research_subreddits = [
    'SaaS', 'startups', 'smallbusiness', 'entrepreneur',
    'productmanagement', 'customer_success', 'sales', 'marketing',
    'devops', 'cloudcomputing', 'dataengineering', 'business_intelligence'
]

# Specific pain points to research
research_topics = {
    'integration': ['integration', 'connect', 'api', 'sync', 'webhook', 'zapier'],
    'data_scattered': ['multiple tools', 'different systems', 'scattered data', 'consolidate', 'centralize'],
    'cost_waste': ['wasting money', 'too expensive', 'cost cutting', 'saas spending', 'budget'],
    'manual_work': ['manual process', 'automate', 'time consuming', 'tedious', 'repetitive'],
    'reporting': ['reporting', 'dashboard', 'analytics', 'metrics', 'kpi'],
    'workflow': ['workflow', 'process', 'efficiency', 'streamline']
}

print("🔍 Researching specific BusinessOS pain points...")

topic_mentions = Counter()
detailed_insights = []

for sub_name in research_subreddits:
    print(f"   Researching r/{sub_name}...", end=" ")
    try:
        subreddit = reddit.subreddit(sub_name)
        found_insights = 0
        
        for post in subreddit.top(time_filter="month", limit=50):
            title_lower = post.title.lower()
            content_lower = post.selftext.lower()
            full_text = title_lower + " " + content_lower
            
            # Check for specific pain points
            for topic, keywords in research_topics.items():
                if any(keyword in full_text for keyword in keywords):
                    topic_mentions[topic] += 1
                    
                    # Store detailed insight
                    detailed_insights.append({
                        'subreddit': sub_name,
                        'topic': topic,
                        'title': post.title,
                        'url': f"https://reddit.com{post.permalink}",
                        'upvotes': post.score,
                        'keywords_found': [k for k in keywords if k in full_text]
                    })
                    found_insights += 1
        
        print(f"✅ {found_insights} insights")
        
    except Exception as e:
        print(f"❌ skipped")
        continue

print(f"\n📊 Found {len(detailed_insights)} detailed pain points")

# Analyze results
print("\n🏆 TOP BUSINESSOS PAIN POINTS:")
print("=" * 40)

for topic, count in topic_mentions.most_common():
    print(f"   {topic:15} - {count} mentions")

print("\n💡 SPECIFIC INSIGHTS FOR BUSINESSOS DEVELOPMENT:")
print("=" * 50)

# Group insights by topic
insights_by_topic = {}
for insight in detailed_insights:
    topic = insight['topic']
    if topic not in insights_by_topic:
        insights_by_topic[topic] = []
    insights_by_topic[topic].append(insight)

# Show top insights for each topic
for topic, insights in insights_by_topic.items():
    if topic_mentions[topic] >= 5:  # Only show significant topics
        print(f"\n🎯 {topic.upper()} PAIN POINTS:")
        top_insights = sorted(insights, key=lambda x: x['upvotes'], reverse=True)[:3]
        for insight in top_insights:
            print(f"   • {insight['title']}")
            print(f"     🔗 {insight['url']}")
            print(f"     👍 {insight['upvotes']} upvotes | Keywords: {', '.join(insight['keywords_found'][:3])}")

print(f"\n✅ Research complete! Use these insights to prioritize BusinessOS features.")
print("💡 Build the features that solve the most mentioned pain points first!")
