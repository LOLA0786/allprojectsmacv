import praw
import pandas as pd
from collections import Counter
import re

print("🔍 RESEARCHING DUBAI/UAE PREMIUM AI PROBLEMS - PEOPLE WILLING TO PAY")
print("=" * 70)

reddit = praw.Reddit(
    client_id="qJyO9FoYahDuWnqG-JG5BA",
    client_secret="N2zF1Rj9HiIGDB2kfKxhmPO0m9A-gA",
    user_agent="DubaiAI_Research v1.0"
)

# Premium problems Dubai/UAE residents will pay to solve
premium_problems = {
    'business_setup': [
        'Dubai business setup', 'UAE company formation', 'freezone setup cost',
        'Dubai license cost', 'business visa UAE', 'PRO services expensive',
        'Dubai mainland license', 'company formation agent'
    ],
    'real_estate_investment': [
        'Dubai real estate investment', 'buy property Dubai', 'off plan investment',
        'Dubai property ROI', 'real estate broker fees', 'property management Dubai',
        'rental yield Dubai', 'mortgage UAE'
    ],
    'gold_visa_services': [
        'golden visa UAE', 'investor visa Dubai', 'UAE residency',
        'long term visa', 'property investment visa', 'entrepreneur visa Dubai'
    ],
    'luxury_services': [
        'yacht rental Dubai', 'luxury car rental', 'personal concierge Dubai',
        'exclusive events Dubai', 'premium services UAE', 'VIP treatment Dubai'
    ],
    'wealth_management': [
        'wealth management Dubai', 'investment advisory UAE', 'tax planning Dubai',
        'family office setup', 'private banking UAE', 'offshore setup Dubai'
    ],
    'education_consulting': [
        'international schools Dubai', 'university admissions UAE',
        'education consultants Dubai', 'school fees Dubai', 'IB tutors Dubai'
    ],
    'healthcare_premium': [
        'medical tourism Dubai', 'premium healthcare UAE', 'executive health check',
        'private hospitals Dubai', 'medical second opinion', 'health insurance UAE'
    ],
    'tech_automation': [
        'business automation Dubai', 'AI solutions UAE', 'digital transformation',
        'smart home Dubai', 'business process automation', 'CRM setup Dubai'
    ],
    'legal_compliance': [
        'UAE legal services', 'compliance Dubai', 'corporate law UAE',
        'contract review Dubai', 'dispute resolution UAE', 'legal consultation'
    ],
    'personal_assistants': [
        'personal assistant Dubai', 'executive assistant', 'lifestyle manager',
        'concierge services', 'personal errands Dubai', 'time saving services'
    ]
}

print("🔍 Scraping premium Dubai/UAE problems...")

dubai_problems_data = []
problem_categories = Counter()
payment_willingness = Counter()
urgency_levels = Counter()

# Target Dubai/UAE and business-focused subreddits
target_subreddits = [
    'dubai', 'UAE', 'abudhabi', 'sharjah',
    'entrepreneur', 'startups', 'fatFIRE', 'expat',
    'digitalnomad', 'investing', 'smallbusiness'
]

for sub_name in target_subreddits:
    print(f"\n🎯 Researching r/{sub_name}...")
    try:
        subreddit = reddit.subreddit(sub_name)
        
        # Search for premium problems
        for category, keywords in premium_problems.items():
            for keyword in keywords:
                try:
                    for post in reddit.subreddit(sub_name).search(keyword, limit=15):
                        title_lower = post.title.lower()
                        content_lower = post.selftext.lower()
                        full_text = title_lower + " " + content_lower
                        
                        # Focus on posts showing willingness to pay
                        if (post.score > 5 and 
                            any(word in full_text for word in ['pay', 'cost', 'price', 'budget', 'invest', 'fee', 'expensive'])):
                            
                            problem_data = {
                                'subreddit': sub_name,
                                'title': post.title,
                                'content': post.selftext[:400],
                                'upvotes': post.score,
                                'comments': post.num_comments,
                                'url': f"https://reddit.com{post.permalink}",
                                'problem_category': category,
                                'urgency': 'medium',
                                'payment_willingness': 'unknown',
                                'budget_indication': [],
                                'problem_complexity': [],
                                'ai_solution_potential': []
                            }
                            
                            # Urgency analysis
                            if any(word in full_text for word in ['urgent', 'asap', 'immediately', 'emergency', 'quick']):
                                problem_data['urgency'] = 'high'
                                urgency_levels['high'] += 1
                            elif any(word in full_text for word in ['soon', 'planning', 'future', 'next month']):
                                problem_data['urgency'] = 'low'
                                urgency_levels['low'] += 1
                            else:
                                urgency_levels['medium'] += 1
                            
                            # Payment willingness analysis
                            if any(word in full_text for word in ['willing to pay', 'ready to invest', 'budget available', 'pay for service']):
                                problem_data['payment_willingness'] = 'high'
                                payment_willingness['high'] += 1
                            elif any(word in full_text for word in ['expensive', 'too costly', 'overpriced', 'high fees']):
                                problem_data['payment_willingness'] = 'medium'  # Will pay for better value
                                payment_willingness['medium'] += 1
                            else:
                                payment_willingness['unknown'] += 1
                            
                            # Budget analysis
                            budget_patterns = [
                                r'\$(\d+,?\d+)', r'AED\s*(\d+,?\d+)', r'(\d+,?\d+)\s*(?:dollars|USD|AED)',
                                r'budget.*?\$(\d+)', r'invest.*?\$(\d+)', r'cost.*?\$(\d+)'
                            ]
                            for pattern in budget_patterns:
                                matches = re.findall(pattern, full_text, re.IGNORECASE)
                                if matches:
                                    problem_data['budget_indication'].extend(matches)
                            
                            # Problem complexity (AI potential)
                            if any(word in full_text for word in ['complicated', 'complex', 'time consuming', 'paperwork', 'process']):
                                problem_data['problem_complexity'].append('high_complexity')
                            if any(word in full_text for word in ['research', 'compare', 'analysis', 'decision']):
                                problem_data['problem_complexity'].append('research_intensive')
                            if any(word in full_text for word in ['multiple options', 'many choices', 'confusing']):
                                problem_data['problem_complexity'].append('decision_fatigue')
                            
                            # AI solution potential
                            if any(word in full_text for word in ['automate', 'streamline', 'efficient', 'fast', 'instant']):
                                problem_data['ai_solution_potential'].append('automation')
                            if any(word in full_text for word in ['compare', 'analysis', 'data', 'research']):
                                problem_data['ai_solution_potential'].append('data_analysis')
                            if any(word in full_text for word in ['recommend', 'suggest', 'best option', 'advice']):
                                problem_data['ai_solution_potential'].append('recommendation_engine')
                            if any(word in full_text for word in ['calculate', 'estimate', 'project', 'forecast']):
                                problem_data['ai_solution_potential'].append('prediction')
                            
                            problem_categories[category] += 1
                            dubai_problems_data.append(problem_data)
                            print(f"   💰 {category}: {post.title[:80]}...")
                            
                except Exception as e:
                    continue
        
        # Get highly engaged Dubai/UAE discussions
        for post in subreddit.top(time_filter="month", limit=25):
            if post.score > 50 and any(word in post.title.lower() for word in ['dubai', 'uae', 'abudhabi']):
                if any(keyword in post.title.lower() + post.selftext.lower() for keyword in ['service', 'consultant', 'advisor', 'agent', 'fee']):
                    # Avoid duplicates
                    if not any(p['url'] == f"https://reddit.com{post.permalink}" for p in dubai_problems_data):
                        problem_data = {
                            'subreddit': sub_name,
                            'title': post.title,
                            'content': post.selftext[:400],
                            'upvotes': post.score,
                            'comments': post.num_comments,
                            'url': f"https://reddit.com{post.permalink}",
                            'problem_category': 'premium_services',
                            'urgency': 'medium',
                            'payment_willingness': 'high',
                            'budget_indication': [],
                            'problem_complexity': [],
                            'ai_solution_potential': []
                        }
                        dubai_problems_data.append(problem_data)
                        print(f"   🔥 Premium service discussion: {post.title[:80]}...")
    
    except Exception as e:
        print(f"   ❌ Error in r/{sub_name}: {e}")
        continue

print(f"\n📊 DUBAI/UAE PREMIUM PROBLEMS RESEARCH:")
print("=" * 60)
print(f"Total premium problems analyzed: {len(dubai_problems_data)}")
print(f"Problem categories identified: {len(problem_categories)}")

print(f"\n🎯 PREMIUM PROBLEM CATEGORIES:")
for category, count in problem_categories.most_common():
    print(f"   {category:25} - {count} discussions")

print(f"\n💰 PAYMENT WILLINGNESS:")
for willingness, count in payment_willingness.most_common():
    print(f"   {willingness:15} - {count} posts")

print(f"\n⏰ URGENCY LEVELS:")
for urgency, count in urgency_levels.most_common():
    print(f"   {urgency:15} - {count} posts")

# Analyze budget indications
budget_data = []
for problem in dubai_problems_data:
    if problem['budget_indication']:
        budget_data.extend(problem['budget_indication'])

print(f"\n💵 BUDGET INDICATIONS:")
budget_counter = Counter(budget_data)
for budget, count in budget_counter.most_common(15):
    print(f"   ${budget:10} - {count} mentions")

# Analyze AI solution potential
ai_potential = Counter()
for problem in dubai_problems_data:
    for potential in problem['ai_solution_potential']:
        ai_potential[potential] += 1

print(f"\n🤖 AI SOLUTION POTENTIAL:")
for solution, count in ai_potential.most_common():
    print(f"   {solution:25} - {count} opportunities")

print(f"\n🚀 HIGH-VALUE AI OPPORTUNITIES IN DUBAI:")
print("=" * 50)

# Find the most valuable problems (high payment willingness + high urgency)
high_value_problems = [
    p for p in dubai_problems_data 
    if p['payment_willingness'] in ['high', 'medium'] and p['urgency'] == 'high'
]
high_value_problems.sort(key=lambda x: x['upvotes'], reverse=True)

print(f"\n💎 TOP HIGH-VALUE PROBLEMS (People Ready to Pay):")
for i, problem in enumerate(high_value_problems[:10], 1):
    print(f"\n{i}. {problem['title']}")
    print(f"   🔗 r/{problem['subreddit']} | 👍 {problem['upvotes']} | 💬 {problem['comments']}")
    print(f"   🎯 Category: {problem['problem_category']}")
    print(f"   💰 Payment willingness: {problem['payment_willingness']}")
    print(f"   ⏰ Urgency: {problem['urgency']}")
    if problem['budget_indication']:
        print(f"   💵 Budget mentioned: {problem['budget_indication'][:3]}")
    if problem['ai_solution_potential']:
        print(f"   🤖 AI solution: {', '.join(problem['ai_solution_potential'])}")
    print(f"   📎 {problem['url']}")

# Save detailed analysis
import os
os.makedirs('dubai_ai_analysis', exist_ok=True)

df = pd.DataFrame(dubai_problems_data)
df.to_csv('dubai_ai_analysis/dubai_premium_problems.csv', index=False)

print(f"\n📁 Detailed analysis saved to 'dubai_ai_analysis/dubai_premium_problems.csv'")

print(f"\n🎯 PREMIUM AI BUSINESS OPPORTUNITIES FOR DUBAI:")
print("=" * 55)

# Generate premium AI business ideas
total_problems = len(dubai_problems_data)
high_payment = payment_willingness['high']
medium_payment = payment_willingness['medium']

print(f"""
📊 MARKET SIZE VALIDATION:
   - {total_problems} premium problems identified
   - {high_payment} explicitly willing to pay premium
   - {medium_payment} willing to pay for better value
   - Average budget indications: ${sum(int(b) for b in budget_data if b.isdigit()) / len([b for b in budget_data if b.isdigit()]):.0f}+

🚀 TOP 5 PREMIUM AI SOLUTIONS FOR DUBAI:

1. **AI BUSINESS SETUP ADVISOR** ({problem_categories['business_setup']} demands)
   - Automated company formation process
   - License type recommendation engine
   - Cost optimization AI
   - Price: $999-2,999 per setup

2. **SMART REAL ESTATE INVESTMENT AI** ({problem_categories['real_estate_investment']} demands)
   - ROI prediction engine
   - Property valuation AI
   - Investment opportunity scoring
   - Price: 1-2% of investment value

3. **GOLDEN VISA ELIGIBILITY OPTIMIZER** ({problem_categories['gold_visa_services']} demands)
   - Eligibility assessment AI
   - Document preparation automation
   - Application success predictor
   - Price: $1,499-3,999

4. **WEALTH MANAGEMENT AI PLATFORM** ({problem_categories['wealth_management']} demands)
   - Personalized investment strategies
   - Tax optimization algorithms
   - Portfolio risk analysis
   - Price: $5,000-20,000/year

5. **PREMIUM CONCIERGE AI** ({problem_categories['luxury_services']} demands)
   - Lifestyle optimization engine
   - Service recommendation AI
   - Automated booking and coordination
   - Price: $499-1,999/month

💡 UNIQUE DUBAI ADVANTAGES:
   - High disposable income
   - Tech-savvy population
   - Business-friendly environment
   - Willingness to pay for premium services
   - Strong demand for automation and efficiency

🎯 TARGET CUSTOMER PROFILE:
   - High-net-worth individuals
   - Entrepreneurs and investors
   - Expatriates needing local services
   - Businesses expanding to UAE
   - Luxury service consumers

💰 PRICING STRATEGY:
   - Premium pricing ($500-5,000+)
   - Value-based pricing models
   - Subscription options for ongoing services
   - Tiered packages (Basic, Pro, Enterprise)
""")

print(f"\n🔥 IMMEDIATE OPPORTUNITIES (90-Day Launch):")
top_categories = problem_categories.most_common(3)
for i, (category, count) in enumerate(top_categories, 1):
    print(f"   {i}. {category.replace('_', ' ').title()} - {count} validated demands")

print(f"\n🎯 RECOMMENDED FIRST MVP:")
most_promising = problem_categories.most_common(1)[0]
print(f"   Build: AI {most_promising[0].replace('_', ' ').title()} Platform")
print(f"   Market Size: {most_promising[1]} immediate demands")
print(f"   Price Point: $1,000-3,000 per solution")
print(f"   Timeline: 6-8 weeks to MVP")
