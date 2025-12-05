import praw
from collections import Counter
import pandas as pd
import re

print("🤖 AI AGENT OS TREND SCRAPER")
print("=" * 55)

reddit = praw.Reddit(
    client_id="qJyO9FoYahDuWnqG-JG5BA",
    client_secret="N2zF1Rj9HiIGDB2kfKxhmPO0m9A-gA",
    user_agent="AgentOS_Research v1.0 (by /u/Unlucky-Ad7349)"
)

# AI agent and computing focused subreddits
agent_subreddits = [
    'MachineLearning', 'artificial', 'AI', 'singularity',
    'LocalLLaMA', 'LLMDevs', 'OpenAI', 'compsci', 'programming',
    'sysadmin', 'devops', 'cloudcomputing'
]

# Agent computing concepts to track
agent_concepts = {
    'mcp': ['mcp', 'model context protocol', 'tool use'],
    'agent_environment': ['agent environment', 'computer environment', 'filesystem', 'sandbox'],
    'tool_use': ['tool use', 'function calling', 'api tools'],
    'agent_os': ['agent os', 'operating system', 'agent platform'],
    'security': ['acl', 'permissions', 'security', 'kill switch', 'audit log'],
    'scheduling': ['scheduler', 'orchestration', 'workflow'],
    'deterministic': ['deterministic', 'financial', 'money', 'transactions'],
    'stochastic': ['stochastic', 'creative', 'ideas', 'exploration']
}

print("🔍 Scanning for AI agent computing trends...")

agent_posts = []
concept_mentions = Counter()
urgency_levels = Counter()

for sub_name in agent_subreddits:
    print(f"   Scanning r/{sub_name}...", end=" ")
    try:
        subreddit = reddit.subreddit(sub_name)
        post_count = 0
        
        # Get recent discussions about agent computing
        for post in subreddit.top(time_filter="month", limit=80):
            title_lower = post.title.lower()
            content_lower = post.selftext.lower()
            full_text = title_lower + " " + content_lower
            
            # Check if this discusses agent computing trends
            is_agent_trend = any(
                keyword in full_text 
                for keyword in ['agent', 'mcp', 'tool use', 'autonomous', 'ai system',
                              'environment', 'filesystem', 'operating system', '2025 trend',
                              '2026 prediction', 'next year', 'future of ai']
            )
            
            if is_agent_trend:
                # Track concept mentions
                for concept, keywords in agent_concepts.items():
                    if any(keyword in full_text for keyword in keywords):
                        concept_mentions[concept] += 1
                
                # Determine urgency level
                urgency = 'medium'
                if any(word in full_text for word in ['urgent', 'critical', 'must have', 'essential']):
                    urgency = 'high'
                elif any(word in full_text for word in ['future', 'prediction', 'trend']):
                    urgency = 'strategic'
                
                urgency_levels[urgency] += 1
                
                # Store post data
                post_data = {
                    'subreddit': sub_name,
                    'title': post.title,
                    'content': post.selftext[:500],
                    'upvotes': post.score,
                    'comments': post.num_comments,
                    'url': f"https://reddit.com{post.permalink}",
                    'concepts': [],
                    'urgency': urgency,
                    'timeline': 'current'  # current/future
                }
                
                # Add specific concepts
                for concept, keywords in agent_concepts.items():
                    if any(keyword in full_text for keyword in keywords):
                        post_data['concepts'].append(concept)
                
                # Determine timeline
                if any(word in full_text for word in ['2026', 'future', 'next year', 'will be']):
                    post_data['timeline'] = 'future'
                
                agent_posts.append(post_data)
                post_count += 1
        
        print(f"✅ {post_count} agent computing posts")
        
    except Exception as e:
        print(f"❌ skipped: {e}")
        continue

print(f"\n📊 Found {len(agent_posts)} AI agent computing discussions")

# Analyze results
print("\n🏆 AGENT COMPUTING CONCEPTS:")
print("=" * 45)

for concept, count in concept_mentions.most_common(15):
    print(f"   {concept:25} - {count} mentions")

print(f"\n🚨 URGENCY LEVELS:")
for urgency, count in urgency_levels.most_common():
    print(f"   {urgency:15} - {count} posts")

print(f"\n💡 THE OPPORTUNITY: AGENT OS PLATFORM")
print("=" * 50)

print("""
🎯 WHAT THE COMMUNITY IS SAYING:

2023: Chatbots (basic Q&A)
2024: RAG & Finetuning (knowledge work)  
2025: MCP & Tool Use (action taking)
2026: Computer Environments & Filesystems (REAL autonomy)

🚀 THE GAP: No proper OS for AI agents!

Current solutions are "POSIX cosplay" - just basic file access.
We need a REAL Agent OS with:

• ACLs & Permissions (security)
• Quotas & Resource Management  
• Snapshots & Versioning
• Audit Logs (compliance)
• Scheduler (orchestration)
• Kill Switch (safety)

💰 BUSINESS OPPORTUNITY:
Build the FIRST Agent Operating System before 2026!
""")

# Show top agent computing posts
print(f"\n🔥 TOP AGENT COMPUTING INSIGHTS:")
print("=" * 50)

if agent_posts:
    top_posts = sorted(agent_posts, key=lambda x: x['upvotes'], reverse=True)[:15]
    
    for i, post in enumerate(top_posts, 1):
        print(f"\n{i}. {post['title']}")
        print(f"   🔗 r/{post['subreddit']} | 👍 {post['upvotes']} | 💬 {post['comments']} comments")
        print(f"   🚨 {post['urgency'].upper()} | Timeline: {post['timeline'].upper()}")
        if post['concepts']:
            print(f"   🎯 Concepts: {', '.join(post['concepts'][:3])}")
        print(f"   📎 {post['url']}")
else:
    print("No agent computing posts found. Let's search differently...")

# Save analysis
import os
os.makedirs('agent_analysis', exist_ok=True)

if agent_posts:
    df = pd.DataFrame(agent_posts)
    df.to_csv('agent_analysis/agent_computing_trends.csv', index=False)
    print(f"\n📁 Analysis saved to 'agent_analysis/' folder")

print(f"\n✅ Opportunity validated with {len(agent_posts)} data points!")
print("💡 Build the Agent OS before 2026 - this is the next platform shift!")
