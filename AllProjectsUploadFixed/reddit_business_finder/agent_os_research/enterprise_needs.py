import praw
import re

print("🏢 ENTERPRISE NEEDS RESEARCH")
print("=" * 50)

reddit = praw.Reddit(
    client_id="qJyO9FoYahDuWnqG-JG5BA",
    client_secret="N2zF1Rj9HiIGDB2kfKxhmPO0m9A-gA", 
    user_agent="Enterprise_Needs v1.0 (by /u/Unlucky-Ad7349)"
)

print("🔍 Researching enterprise requirements and budgets...")

# Enterprise-focused search terms
enterprise_searches = [
    "enterprise AI security requirements",
    "compliance for AI systems", 
    "GDPR AI compliance",
    "HIPAA machine learning",
    "SOC 2 AI platform",
    "enterprise budget AI",
    "vendor selection AI",
    "IT procurement AI"
]

enterprise_requirements = []
budget_mentions = []

print("\n🎯 Analyzing enterprise discussions...")

for search_term in enterprise_searches:
    print(f"   Searching: '{search_term}'")
    try:
        for post in reddit.subreddit("all").search(search_term, limit=10):
            # Look for enterprise context
            if any(word in post.subreddit.display_name.lower() for word in ['enterprise', 'business', 'startup', 'tech']):
                content_lower = post.selftext.lower()
                
                requirement = {
                    'title': post.title,
                    'subreddit': post.subreddit.display_name,
                    'upvotes': post.score,
                    'url': f"https://reddit.com{post.permalink}",
                    'requirements': [],
                    'budget_mentioned': False,
                    'compliance_mentioned': False
                }
                
                # Extract specific requirements
                if any(word in content_lower for word in ['security', 'access control', 'permission']):
                    requirement['requirements'].append('security')
                if any(word in content_lower for word in ['compliance', 'gdpr', 'hipaa', 'soc2']):
                    requirement['requirements'].append('compliance')
                    requirement['compliance_mentioned'] = True
                if any(word in content_lower for word in ['audit', 'logging', 'tracking']):
                    requirement['requirements'].append('audit_trail')
                if any(word in content_lower for word in ['budget', 'cost', 'price', '$']):
                    requirement['budget_mentioned'] = True
                    budget_mentions.append(post.title)
                
                enterprise_requirements.append(requirement)
                print(f"      ✅ Enterprise need: {post.title[:80]}...")
                
    except Exception as e:
        continue

print(f"\n📊 ENTERPRISE REQUIREMENTS ANALYSIS:")
print(f"Total enterprise discussions: {len(enterprise_requirements)}")

requirements_count = {}
for req in enterprise_requirements:
    for r in req['requirements']:
        requirements_count[r] = requirements_count.get(r, 0) + 1

print(f"\n🎯 TOP ENTERPRISE REQUIREMENTS:")
for req, count in sorted(requirements_count.items(), key=lambda x: x[1], reverse=True):
    print(f"   {req:20} - {count} mentions")

compliance_count = sum(1 for r in enterprise_requirements if r['compliance_mentioned'])
budget_count = sum(1 for r in enterprise_requirements if r['budget_mentioned'])

print(f"\n💰 ENTERPRISE SPENDING INDICATORS:")
print(f"   Budget discussions: {budget_count}")
print(f"   Compliance requirements: {compliance_count}")

print(f"\n🏢 ENTERPRISE PAIN POINTS:")
enterprise_pains = [
    "Security teams blocking AI adoption",
    "Compliance requirements slowing innovation", 
    "Lack of audit trails for AI decisions",
    "No enterprise-grade AI platforms",
    "Budget constraints for AI infrastructure",
    "Vendor lock-in concerns",
    "Data privacy and sovereignty issues"
]

for i, pain in enumerate(enterprise_pains, 1):
    print(f"{i}. {pain}")

print(f"\n🎯 TARGET ENTERPRISE SEGMENTS:")
segments = {
    'Financial Services': "Highest budget, most compliance needs",
    'Healthcare': "HIPAA compliance, high security requirements", 
    'Government': "Security, audit trails, compliance focus",
    'Enterprise Tech': "Scale, reliability, integration needs",
    'E-commerce': "Cost-sensitive, need reliability"
}

for segment, description in segments.items():
    print(f"\n💼 {segment}:")
    print(f"   {description}")

print(f"\n🚀 ENTERPRISE SALES STRATEGY:")
print("""
1. **Start with Compliance-First Industries**
   - Financial services, healthcare, government
   - Higher budgets, urgent needs

2. **Focus on Security & Audit Requirements**
   - Address CISO and compliance officer concerns
   - Provide detailed audit trails and access controls

3. **Price for Enterprise Value**
   - $50k-500k/year for mid-market
   - $500k-2M+/year for large enterprises
   - Focus on ROI from prevented outages and security incidents

4. **Leverage Existing Infrastructure**
   - Integrate with Kubernetes, Docker, AWS
   - Don't require rip-and-replace
   - Position as security/add-on layer
""")
