import praw
import pandas as pd
from collections import Counter
import re

print("🔍 RESEARCHING NORTH AMERICA AI AUTOMATION GAPS & UNTAPPED INDUSTRIES")
print("=" * 70)

reddit = praw.Reddit(
    client_id="qJyO9FoYahDuWnqG-JG5BA",
    client_secret="N2zF1Rj9HiIGDB2kfKxhmPO0m9A-gA",
    user_agent="NorthAmericaAI_Gaps v1.0"
)

# Industries lagging in AI adoption + automation pain points
automation_gaps_research = {
    'manual_labor_industries': [
        'construction manual work', 'landscaping automation', 'plumbing tech',
        'electrician software', 'roofing technology', 'contractor software',
        'trades automation', 'skilled labor tech', 'field service software'
    ],
    'traditional_manufacturing': [
        'small manufacturing automation', 'factory legacy systems',
        'industrial automation small business', 'manufacturing software old',
        'production line manual', 'quality control manual', 'assembly line tech'
    ],
    'agriculture_farming': [
        'farming automation', 'agriculture tech small farm', 
        'ranch management software', 'crop monitoring manual',
        'livestock tracking', 'farm equipment automation', 'precision agriculture'
    ],
    'local_services': [
        'cleaning service software', 'lawn care automation',
        'handyman scheduling', 'local contractor tech', 
        'service business automation', 'home services software'
    ],
    'healthcare_manual': [
        'medical practice automation', 'clinic manual processes',
        'healthcare paperwork automation', 'medical records manual',
        'patient scheduling old', 'healthcare admin software'
    ],
    'education_traditional': [
        'school administration manual', 'teacher paperwork automation',
        'education tech gap', 'classroom management software',
        'school district legacy systems'
    ],
    'government_legacy': [
        'government automation', 'public sector legacy systems',
        'municipal software old', 'city services automation',
        'government paperwork manual'
    ],
    'retail_small_business': [
        'small retail automation', 'brick and mortar tech',
        'inventory management manual', 'retail paperwork automation',
        'local store software'
    ],
    'food_industry': [
        'restaurant automation', 'food truck software',
        'bakery management manual', 'catering business tech',
        'food service automation'
    ],
    'transportation_logistics': [
        'trucking company software', 'logistics manual processes',
        'shipping paperwork automation', 'fleet management legacy',
        'transportation admin manual'
    ]
}

# Specific automation pain points
automation_pain_points = {
    'paperwork_manual': [
        'manual data entry', 'paper forms', 'excel spreadsheets',
        'manual reporting', 'paper invoices', 'manual scheduling'
    ],
    'communication_gaps': [
        'phone calls back and forth', 'email chains', 'text message scheduling',
        'communication breakdown', 'missed messages', 'coordination issues'
    ],
    'legacy_software': [
        'old software', 'legacy systems', 'outdated technology',
        'software not talking', 'integration issues', 'compatibility problems'
    ],
    'cost_barriers': [
        'automation too expensive', 'software cost prohibitive',
        'can\'t afford automation', 'small business budget tech',
        'ROI not clear automation'
    ],
    'skill_gaps': [
        'not tech savvy', 'don\'t understand automation', 'training needed',
        'learning curve too steep', 'staff can\'t use software'
    ]
}

print("🔍 Scraping North America AI automation gaps...")

automation_gaps_data = []
industry_gaps = Counter()
automation_pains = Counter()
adoption_barriers = Counter()

# Target industry-specific and small business subreddits
target_subreddits = [
    'smallbusiness', 'entrepreneur', 'startups', 'manufacturing',
    'construction', 'electricians', 'plumbing', 'HVAC',
    'farming', 'agriculture', 'restaurantowners', 'foodtrucks',
    'trucking', 'logistics', 'healthcare', 'teachers',
    'government', 'municipal', 'retail', 'localbusiness',
    'contractor', 'landscaping', 'cleaningbusiness', 'handyman',
    'techsupport', 'automation', 'sysadmin'
]

for sub_name in target_subreddits:
    print(f"\n🎯 Researching r/{sub_name}...")
    try:
        subreddit = reddit.subreddit(sub_name)
        
        # Search for automation gaps and manual process complaints
        for category, keywords in automation_gaps_research.items():
            for keyword in keywords:
                try:
                    for post in reddit.subreddit(sub_name).search(keyword, limit=12):
                        title_lower = post.title.lower()
                        content_lower = post.selftext.lower()
                        full_text = title_lower + " " + content_lower
                        
                        # Focus on posts discussing manual processes or tech gaps
                        if (post.score > 3 and 
                            any(word in full_text for word in ['manual', 'automate', 'software', 'tech', 'system', 'process', 'efficient'])):
                            
                            gap_data = {
                                'subreddit': sub_name,
                                'title': post.title,
                                'content': post.selftext[:400],
                                'upvotes': post.score,
                                'comments': post.num_comments,
                                'url': f"https://reddit.com{post.permalink}",
                                'industry_category': category,
                                'automation_gap_level': 'medium',
                                'main_pain_points': [],
                                'adoption_barriers': [],
                                'tech_sophistication': 'low',
                                'willingness_to_automate': 'unknown',
                                'budget_indication': []
                            }
                            
                            # Automation gap level
                            if any(word in full_text for word in ['completely manual', 'all paper', 'no software', 'spreadsheets']):
                                gap_data['automation_gap_level'] = 'high'
                            elif any(word in full_text for word in ['some automation', 'basic software', 'partial']):
                                gap_data['automation_gap_level'] = 'low'
                            
                            # Main pain points
                            for pain_category, pain_keywords in automation_pain_points.items():
                                if any(word in full_text for word in pain_keywords):
                                    gap_data['main_pain_points'].append(pain_category)
                                    automation_pains[pain_category] += 1
                            
                            # Adoption barriers
                            if any(word in full_text for word in ['expensive', 'cost', 'price', 'budget', 'afford']):
                                gap_data['adoption_barriers'].append('cost')
                                adoption_barriers['cost'] += 1
                            if any(word in full_text for word in ['complicated', 'complex', 'hard to use', 'learning curve']):
                                gap_data['adoption_barriers'].append('complexity')
                                adoption_barriers['complexity'] += 1
                            if any(word in full_text for word in ['time', 'setup', 'implementation', 'migration']):
                                gap_data['adoption_barriers'].append('time_investment')
                                adoption_barriers['time_investment'] += 1
                            if any(word in full_text for word in ['tech', 'computer', 'digital', 'software knowledge']):
                                gap_data['adoption_barriers'].append('skill_gap')
                                adoption_barriers['skill_gap'] += 1
                            
                            # Tech sophistication
                            if any(word in full_text for word in ['excel', 'paper', 'notebook', 'manual entry']):
                                gap_data['tech_sophistication'] = 'very_low'
                            elif any(word in full_text for word in ['basic software', 'simple app', 'mobile app']):
                                gap_data['tech_sophistication'] = 'low'
                            elif any(word in full_text for word in ['integrated', 'cloud', 'API', 'automation']):
                                gap_data['tech_sophistication'] = 'medium'
                            
                            # Willingness to automate
                            if any(word in full_text for word in ['want to automate', 'need software', 'looking for solution', 'automate this']):
                                gap_data['willingness_to_automate'] = 'high'
                            elif any(word in full_text for word in ['frustrated', 'tired of', 'sick of manual']):
                                gap_data['willingness_to_automate'] = 'medium'
                            
                            # Budget indications
                            budget_patterns = [
                                r'\$(\d+,?\d+)', r'(\d+,?\d+)\s*(?:dollars|USD)',
                                r'budget.*?\$(\d+)', r'cost.*?\$(\d+)', r'pay.*?\$(\d+)'
                            ]
                            for pattern in budget_patterns:
                                matches = re.findall(pattern, full_text, re.IGNORECASE)
                                if matches:
                                    gap_data['budget_indication'].extend(matches)
                            
                            industry_gaps[category] += 1
                            automation_gaps_data.append(gap_data)
                            print(f"   🔧 {category}: {post.title[:70]}...")
                            
                except Exception as e:
                    continue
        
        # Get highly engaged discussions about manual processes
        for post in subreddit.top(time_filter="month", limit=20):
            if post.score > 15:
                manual_keywords = ['manual', 'paperwork', 'spreadsheet', 'excel', 'time consuming', 'inefficient']
                if any(keyword in post.title.lower() + post.selftext.lower() for keyword in manual_keywords):
                    if not any(p['url'] == f"https://reddit.com{post.permalink}" for p in automation_gaps_data):
                        gap_data = {
                            'subreddit': sub_name,
                            'title': post.title,
                            'content': post.selftext[:400],
                            'upvotes': post.score,
                            'comments': post.num_comments,
                            'url': f"https://reddit.com{post.permalink}",
                            'industry_category': 'general_manual_labor',
                            'automation_gap_level': 'high',
                            'main_pain_points': ['paperwork_manual'],
                            'adoption_barriers': [],
                            'tech_sophistication': 'low',
                            'willingness_to_automate': 'high',
                            'budget_indication': []
                        }
                        automation_gaps_data.append(gap_data)
                        print(f"   📋 Manual process complaint: {post.title[:70]}...")
    
    except Exception as e:
        print(f"   ❌ Error in r/{sub_name}: {e}")
        continue

print(f"\n📊 NORTH AMERICA AI AUTOMATION GAPS RESEARCH:")
print("=" * 60)
print(f"Total automation gaps identified: {len(automation_gaps_data)}")
print(f"Industries with major gaps: {len(industry_gaps)}")

print(f"\n🏭 INDUSTRIES WITH MAJOR AUTOMATION GAPS:")
for industry, count in industry_gaps.most_common():
    print(f"   {industry:30} - {count} gaps identified")

print(f"\n😫 TOP AUTOMATION PAIN POINTS:")
for pain, count in automation_pains.most_common():
    print(f"   {pain:25} - {count} mentions")

print(f"\n🚧 ADOPTION BARRIERS:")
for barrier, count in adoption_barriers.most_common():
    print(f"   {barrier:20} - {count} mentions")

# Analyze willingness to automate
willingness = Counter([p['willingness_to_automate'] for p in automation_gaps_data])
print(f"\n💡 WILLINGNESS TO AUTOMATE:")
for level, count in willingness.most_common():
    print(f"   {level:15} - {count} businesses")

# Analyze tech sophistication
tech_levels = Counter([p['tech_sophistication'] for p in automation_gaps_data])
print(f"\n💻 CURRENT TECH SOPHISTICATION:")
for level, count in tech_levels.most_common():
    print(f"   {level:15} - {count} businesses")

print(f"\n🚀 HIGH-OPPORTUNITY AUTOMATION TARGETS:")
print("=" * 50)

# Find the best opportunities (high gap + high willingness)
high_opportunity_gaps = [
    p for p in automation_gaps_data 
    if p['automation_gap_level'] in ['high', 'medium'] 
    and p['willingness_to_automate'] in ['high', 'medium']
]
high_opportunity_gaps.sort(key=lambda x: x['upvotes'], reverse=True)

print(f"\n💎 TOP AUTOMATION OPPORTUNITIES (Ready Market):")
for i, gap in enumerate(high_opportunity_gaps[:10], 1):
    print(f"\n{i}. {gap['title']}")
    print(f"   🔗 r/{gap['subreddit']} | 👍 {gap['upvotes']} | 💬 {gap['comments']}")
    print(f"   🏭 Industry: {gap['industry_category']}")
    print(f"   📊 Gap Level: {gap['automation_gap_level']}")
    print(f"   💡 Willingness: {gap['willingness_to_automate']}")
    print(f"   💻 Tech Level: {gap['tech_sophistication']}")
    if gap['main_pain_points']:
        print(f"   😫 Pain Points: {', '.join(gap['main_pain_points'][:3])}")
    if gap['adoption_barriers']:
        print(f"   🚧 Barriers: {', '.join(gap['adoption_barriers'][:2])}")
    print(f"   📎 {gap['url']}")

# Save detailed analysis
import os
os.makedirs('automation_gaps_analysis', exist_ok=True)

df = pd.DataFrame(automation_gaps_data)
df.to_csv('automation_gaps_analysis/north_america_automation_gaps.csv', index=False)

print(f"\n📁 Detailed analysis saved to 'automation_gaps_analysis/north_america_automation_gaps.csv'")

print(f"\n🎯 AI AUTOMATION OPPORTUNITIES - NORTH AMERICA:")
print("=" * 55)

total_gaps = len(automation_gaps_data)
high_willingness = willingness['high'] + willingness['medium']

print(f"""
📊 MARKET SIZE VALIDATION:
   - {total_gaps} automation gaps identified across industries
   - {high_willingness} businesses actively wanting automation solutions
   - Top 3 pain points: {automation_pains.most_common(3)[0][0]}, {automation_pains.most_common(3)[1][0]}, {automation_pains.most_common(3)[2][0]}
   - Main barriers: {adoption_barriers.most_common(2)[0][0]} and {adoption_barriers.most_common(2)[1][0]}

🚀 TOP 5 UNTAPPED AI AUTOMATION MARKETS:

1. **CONSTRUCTION & TRADES AUTOMATION** ({industry_gaps['manual_labor_industries']} gaps)
   - Field service scheduling AI
   - Quote generation automation  
   - Project management for trades
   - Price: $99-299/month

2. **LOCAL SERVICES AUTOMATION** ({industry_gaps['local_services']} gaps)
   - Booking and scheduling AI
   - Customer communication automation
   - Payment processing integration
   - Price: $49-149/month

3. **SMALL MANUFACTURING AI** ({industry_gaps['traditional_manufacturing']} gaps)
   - Production tracking automation
   - Quality control AI
   - Inventory management
   - Price: $199-499/month

4. **AGRICULTURE TECH AUTOMATION** ({industry_gaps['agriculture_farming']} gaps)
   - Crop monitoring AI
   - Equipment maintenance scheduling
   - Yield prediction algorithms
   - Price: $149-349/month

5. **FOOD INDUSTRY AUTOMATION** ({industry_gaps['food_industry']} gaps)
   - Restaurant management AI
   - Inventory optimization
   - Customer loyalty automation
   - Price: $79-199/month

💡 UNIQUE OPPORTUNITIES:

**LOW-HANGING FRUIT**: Industries still using:
   - Paper forms and spreadsheets
   - Manual scheduling via phone/email
   - Basic Excel for inventory
   - Physical notebooks for records

**AI SOLUTIONS NEEDED**:
   - Simple, affordable automation tools
   - Mobile-first solutions (field workers)
   - Integration with existing simple tools
   - Minimal training required

🎯 TARGET CUSTOMER PROFILE:
   - Small business owners in traditional industries
   - Field service businesses (construction, repairs, cleaning)
   - Local service providers
   - Businesses with 2-20 employees
   - Owners frustrated with manual processes

💰 PRICING STRATEGY:
   - Affordable monthly subscriptions ($49-499)
   - Free trials to overcome cost barriers
   - Simple per-user pricing
   - Mobile app included
""")

print(f"\n🔥 IMMEDIATE OPPORTUNITIES (30-Day Launch):")
top_industries = industry_gaps.most_common(3)
for i, (industry, count) in enumerate(top_industries, 1):
    print(f"   {i}. {industry.replace('_', ' ').title()} - {count} validated gaps")

print(f"\n🎯 RECOMMENDED FIRST MVP:")
most_promising = industry_gaps.most_common(1)[0]
print(f"   Build: AI {most_promising[0].replace('_', ' ').title()} Automation")
print(f"   Market Size: {most_promising[1]} immediate needs")
print(f"   Price Point: $99-299/month")
print(f"   Timeline: 4-6 weeks to MVP")
