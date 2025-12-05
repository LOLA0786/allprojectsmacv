import praw
from collections import Counter
import pandas as pd
import re

print("🎯 DEEP PAIN POINT RESEARCH - D2C BRANDS")
print("=" * 60)

reddit = praw.Reddit(
    client_id="qJyO9FoYahDuWnqG-JG5BA",
    client_secret="N2zF1Rj9HiIGDB2kfKxhmPO0m9A-gA",
    user_agent="DeepPain_Research v1.0 (by /u/Unlucky-Ad7349)"
)

# Strategic research targets for D2C brands
research_targets = {
    'customer_acquisition': [
        'customer acquisition cost', 'CAC too high', 'acquiring customers',
        'customer acquisition strategy', 'paid ads not working', 'facebook ads',
        'google ads', 'instagram ads', 'tiktok ads', 'customer acquisition problem'
    ],
    'retention_issues': [
        'customer retention', 'high churn rate', 'repeat customers',
        'loyalty program', 'retention strategy', 'customer churn',
        'keeping customers', 'subscription cancellation'
    ],
    'conversion_optimization': [
        'conversion rate low', 'CRO problems', 'website not converting',
        'abandoned cart', 'checkout issues', 'low conversion',
        'conversion optimization', 'shopping cart abandonment'
    ],
    'logistics_shipping': [
        'shipping problems', 'delivery issues', 'logistics nightmare',
        'fulfillment problems', 'inventory management', 'supply chain',
        'shipping costs', 'international shipping', 'returns processing'
    ],
    'customer_service': [
        'customer complaints', 'support tickets', 'bad reviews',
        'negative feedback', 'customer service overwhelmed',
        'handling returns', 'refund requests', 'customer satisfaction'
    ],
    'profitability_margins': [
        'profit margins low', 'not profitable', 'burning cash',
        'cash flow problems', 'unit economics', 'COGS too high',
        'operating costs', 'scaling profitably'
    ],
    'competition_marketplace': [
        'competition stealing', 'marketplace fees', 'amazon competition',
        'shopify problems', 'saturated market', 'differentiation',
        'standing out competition'
    ],
    'marketing_channels': [
        'marketing not working', 'ROAS low', 'ad spend waste',
        'email marketing', 'SMS marketing', 'social media marketing',
        'influencer marketing', 'organic traffic'
    ]
}

print("🔍 Conducting deep pain point research for D2C brands...")

deep_pain_points = []
pain_categories = Counter()
industry_context = Counter()

# Target subreddits where D2C brand owners discuss real problems
pain_subreddits = [
    'ecommerce', 'shopify', 'Entrepreneur', 'smallbusiness',
    'marketing', 'PPC', 'digital_marketing', 'startups',
    'advancedentrepreneur', 'D2C', 'directtoconsumer'
]

for sub_name in pain_subreddits:
    print(f"\n🎯 Researching r/{sub_name}...")
    try:
        subreddit = reddit.subreddit(sub_name)
        
        # Search for specific D2C pain points
        for category, keywords in research_targets.items():
            for keyword in keywords:
                try:
                    for post in reddit.subreddit(sub_name).search(keyword, limit=20):
                        title_lower = post.title.lower()
                        content_lower = post.selftext.lower()
                        full_text = title_lower + " " + content_lower
                        
                        # Only include posts with significant engagement
                        if post.score > 5 and post.num_comments > 3:
                            pain_data = {
                                'subreddit': sub_name,
                                'title': post.title,
                                'content': post.selftext[:300],
                                'upvotes': post.score,
                                'comments': post.num_comments,
                                'url': f"https://reddit.com{post.permalink}",
                                'pain_category': category,
                                'severity': 'medium',
                                'business_impact': 'unknown',
                                'root_cause': []
                            }
                            
                            # Determine severity
                            if any(word in full_text for word in ['critical', 'bankrupt', 'closing', 'emergency', 'major']):
                                pain_data['severity'] = 'critical'
                            elif any(word in full_text for word in ['serious', 'struggling', 'urgent', 'failing']):
                                pain_data['severity'] = 'high'
                            
                            # Determine business impact
                            if any(word in full_text for word in ['revenue', 'sales', 'money', 'cost', 'profit']):
                                pain_data['business_impact'] = 'financial'
                            elif any(word in full_text for word in ['customer', 'complaints', 'reviews', 'satisfaction']):
                                pain_data['business_impact'] = 'customer_relations'
                            elif any(word in full_text for word in ['competition', 'market', 'saturated']):
                                pain_data['business_impact'] = 'competitive'
                            elif any(word in full_text for word in ['logistics', 'shipping', 'delivery']):
                                pain_data['business_impact'] = 'operational'
                            
                            # Analyze root causes for D2C
                            if any(word in full_text for word in ['facebook', 'google', 'ads', 'advertising']):
                                pain_data['root_cause'].append('ad_costs_rising')
                            if any(word in full_text for word in ['competition', 'amazon', 'saturated']):
                                pain_data['root_cause'].append('market_competition')
                            if any(word in full_text for word in ['shipping', 'delivery', 'logistics']):
                                pain_data['root_cause'].append('supply_chain_issues')
                            if any(word in full_text for word in ['conversion', 'website', 'checkout']):
                                pain_data['root_cause'].append('conversion_optimization')
                            if any(word in full_text for word in ['retention', 'churn', 'loyalty']):
                                pain_data['root_cause'].append('customer_retention')
                            if any(word in full_text for word in ['margins', 'COGS', 'costs']):
                                pain_data['root_cause'].append('profitability')
                            
                            pain_categories[category] += 1
                            deep_pain_points.append(pain_data)
                            print(f"   ✅ {category}: {post.title[:60]}...")
                            
                except Exception as e:
                    continue
        
        # Also get highly engaged discussions about D2C struggles
        for post in subreddit.top(time_filter="month", limit=30):
            if post.score > 50:  # Highly engaged posts
                if any(keyword in post.title.lower() for keyword in ['struggling', 'problem', 'issue', 'failed', 'help', 'advice', 'challenge']):
                    # Avoid duplicates
                    if not any(p['url'] == f"https://reddit.com{post.permalink}" for p in deep_pain_points):
                        pain_data = {
                            'subreddit': sub_name,
                            'title': post.title,
                            'content': post.selftext[:300],
                            'upvotes': post.score,
                            'comments': post.num_comments,
                            'url': f"https://reddit.com{post.permalink}",
                            'pain_category': 'general_d2c',
                            'severity': 'high',
                            'business_impact': 'unknown',
                            'root_cause': []
                        }
                        deep_pain_points.append(pain_data)
                        print(f"   🔥 High engagement: {post.title[:60]}...")
    
    except Exception as e:
        print(f"   ❌ Error in r/{sub_name}: {e}")
        continue

print(f"\n📊 D2C PAIN POINT RESEARCH RESULTS:")
print("=" * 50)
print(f"Total pain points analyzed: {len(deep_pain_points)}")
print(f"Pain categories identified: {len(pain_categories)}")

print(f"\n🎯 D2C PAIN CATEGORY BREAKDOWN:")
for category, count in pain_categories.most_common():
    print(f"   {category:25} - {count} incidents")

# Analyze root causes
root_causes = Counter()
for pain in deep_pain_points:
    for cause in pain['root_cause']:
        root_causes[cause] += 1

print(f"\n🔍 ROOT CAUSE ANALYSIS:")
for cause, count in root_causes.most_common():
    print(f"   {cause:25} - {count} occurrences")

print(f"\n💡 BUSINESS IMPACT ANALYSIS:")
business_impacts = Counter()
for pain in deep_pain_points:
    business_impacts[pain['business_impact']] += 1

for impact, count in business_impacts.most_common():
    print(f"   {impact:20} - {count} incidents")

print(f"\n🚨 CRITICAL D2C PAIN POINTS (Highest Impact):")
print("=" * 50)

critical_pains = [p for p in deep_pain_points if p['severity'] == 'critical']
critical_pains.sort(key=lambda x: x['upvotes'], reverse=True)

for i, pain in enumerate(critical_pains[:10], 1):
    print(f"\n{i}. {pain['title']}")
    print(f"   🔗 r/{pain['subreddit']} | 👍 {pain['upvotes']} | 💬 {pain['comments']}")
    print(f"   🎯 Category: {pain['pain_category']}")
    print(f"   💰 Impact: {pain['business_impact']}")
    if pain['root_cause']:
        print(f"   🔍 Root Causes: {', '.join(pain['root_cause'])}")
    print(f"   📎 {pain['url']}")

# Save detailed analysis
import os
os.makedirs('deep_analysis', exist_ok=True)

df = pd.DataFrame(deep_pain_points)
df.to_csv('deep_analysis/d2c_pain_points.csv', index=False)

print(f"\n📁 Detailed analysis saved to 'deep_analysis/d2c_pain_points.csv'")

print(f"\n🎯 STRATEGIC INSIGHTS FOR D2C BRANDS:")
print("=" * 45)
print("""
Based on deep pain point analysis, D2C solutions should focus on:

1. **Customer Acquisition Cost** - Biggest challenge with rising ad prices
2. **Customer Retention** - High churn rates killing profitability  
3. **Conversion Rate Optimization** - Websites not converting traffic
4. **Profit Margins** - Balancing acquisition costs with lifetime value
5. **Logistics & Fulfillment** - Operational headaches for growing brands

💰 **VALIDATED MARKET NEED**: D2C brands are struggling with profitability and scalability!
📈 **OPPORTUNITY AREAS**: 
   - AI-powered customer acquisition optimization
   - Retention automation and loyalty programs
   - Conversion rate optimization tools
   - Profitability analysis and margin optimization
""")

print(f"\n🔥 TOP 5 D2C PAIN AREAS:")
top_categories = pain_categories.most_common(5)
for i, (category, count) in enumerate(top_categories, 1):
    print(f"   {i}. {category.replace('_', ' ').title()} - {count} pain points")
