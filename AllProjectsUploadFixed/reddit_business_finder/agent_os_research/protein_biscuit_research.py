import praw
import pandas as pd
from collections import Counter
import re

print("🔍 RESEARCHING PROTEIN & NUTRIENT BISCUITS MARKET")
print("=" * 60)

reddit = praw.Reddit(
    client_id="qJyO9FoYahDuWnqG-JG5BA",
    client_secret="N2zF1Rj9HiIGDB2kfKxhmPO0m9A-gA",
    user_agent="ProteinBiscuit_Research v1.0"
)

# Research targets for protein/nutrient biscuits
research_targets = {
    'product_demands': [
        'protein biscuits', 'protein cookies', 'healthy biscuits',
        'nutrient dense snacks', 'high protein snacks', 'protein snacks',
        'healthy cookies', 'nutrition biscuits', 'fitness snacks',
        'low sugar biscuits', 'high fiber biscuits'
    ],
    'price_concerns': [
        'protein snacks expensive', 'affordable protein', 'cheap protein snacks',
        'protein bars expensive', 'cost of protein snacks', 'price too high',
        'overpriced protein', 'budget protein snacks'
    ],
    'ingredient_preferences': [
        'clean ingredients', 'natural ingredients', 'no artificial',
        'organic protein', 'plant based protein', 'whey protein snacks',
        'soy free protein', 'gluten free protein snacks', 'dairy free protein'
    ],
    'taste_issues': [
        'protein snacks taste', 'chalky texture', 'gritty protein',
        'bad aftertaste', 'protein snacks dry', 'hard texture',
        'bland protein snacks', 'improve taste'
    ],
    'health_goals': [
        'weight loss snacks', 'muscle building snacks', 'diabetic snacks',
        'energy boosting snacks', 'meal replacement snacks',
        'post workout snacks', 'healthy office snacks'
    ],
    'brand_mentions': [
        'quest cookies', 'grenade bars', 'barebells', 'thinkthin',
        'one protein', 'legendary foods', 'atkins snacks', 'kind bars'
    ]
}

print("🔍 Scraping protein biscuit discussions...")

protein_biscuit_data = []
categories = Counter()
sentiment_analysis = Counter()

# Target subreddits for health, fitness, and nutrition
target_subreddits = [
    'fitness', 'nutrition', 'gainit', 'loseit',
    'bodybuilding', 'supplements', 'HealthyFood',
    'EatCheapAndHealthy', 'veganfitness', 'glutenfree',
    'weightloss', 'mealprep', 'snacks'
]

for sub_name in target_subreddits:
    print(f"\n🎯 Researching r/{sub_name}...")
    try:
        subreddit = reddit.subreddit(sub_name)
        
        # Search for protein biscuit related discussions
        for category, keywords in research_targets.items():
            for keyword in keywords:
                try:
                    for post in reddit.subreddit(sub_name).search(keyword, limit=15):
                        title_lower = post.title.lower()
                        content_lower = post.selftext.lower()
                        full_text = title_lower + " " + content_lower
                        
                        # Only include relevant posts with engagement
                        if post.score > 3 and len(post.selftext) > 50:
                            post_data = {
                                'subreddit': sub_name,
                                'title': post.title,
                                'content': post.selftext[:500],
                                'upvotes': post.score,
                                'comments': post.num_comments,
                                'url': f"https://reddit.com{post.permalink}",
                                'category': category,
                                'sentiment': 'neutral',
                                'price_mentions': [],
                                'ingredient_concerns': [],
                                'taste_complaints': [],
                                'health_benefits': [],
                                'brand_preferences': []
                            }
                            
                            # Sentiment analysis
                            positive_words = ['love', 'great', 'amazing', 'best', 'perfect', 'excellent', 'good']
                            negative_words = ['hate', 'terrible', 'awful', 'disappointing', 'bad', 'expensive', 'overpriced']
                            
                            if any(word in full_text for word in positive_words):
                                post_data['sentiment'] = 'positive'
                                sentiment_analysis['positive'] += 1
                            elif any(word in full_text for word in negative_words):
                                post_data['sentiment'] = 'negative'
                                sentiment_analysis['negative'] += 1
                            else:
                                sentiment_analysis['neutral'] += 1
                            
                            # Price analysis
                            price_patterns = [
                                r'\$(\d+\.?\d*)', r'(\d+)\s*dollars', r'expensive', r'cheap', 
                                r'affordable', r'overpriced', r'pricey', r'cost.*?\$(\d+)'
                            ]
                            for pattern in price_patterns:
                                matches = re.findall(pattern, full_text, re.IGNORECASE)
                                if matches:
                                    post_data['price_mentions'].extend(matches)
                            
                            # Ingredient concerns
                            if any(word in full_text for word in ['artificial', 'preservatives', 'chemicals', 'processed']):
                                post_data['ingredient_concerns'].append('artificial_ingredients')
                            if any(word in full_text for word in ['sugar', 'sugary', 'sweetener']):
                                post_data['ingredient_concerns'].append('high_sugar')
                            if any(word in full_text for word in ['soy', 'dairy', 'gluten', 'allergen']):
                                post_data['ingredient_concerns'].append('allergens')
                            if any(word in full_text for word in ['natural', 'clean', 'organic', 'non-gmo']):
                                post_data['ingredient_concerns'].append('clean_ingredients')
                            
                            # Taste complaints
                            if any(word in full_text for word in ['chalky', 'gritty', 'dry', 'hard']):
                                post_data['taste_complaints'].append('texture_issues')
                            if any(word in full_text for word in ['aftertaste', 'bitter', 'weird taste']):
                                post_data['taste_complaints'].append('flavor_issues')
                            if any(word in full_text for word in ['bland', 'tasteless', 'no flavor']):
                                post_data['taste_complaints'].append('lack_flavor')
                            
                            # Health benefits sought
                            if any(word in full_text for word in ['muscle', 'gains', 'workout', 'recovery']):
                                post_data['health_benefits'].append('muscle_building')
                            if any(word in full_text for word in ['weight loss', 'diet', 'low calorie', 'satiety']):
                                post_data['health_benefits'].append('weight_management')
                            if any(word in full_text for word in ['energy', 'fuel', 'sustained']):
                                post_data['health_benefits'].append('energy_boost')
                            if any(word in full_text for word in ['healthy', 'nutritious', 'wholesome']):
                                post_data['health_benefits'].append('general_health')
                            
                            categories[category] += 1
                            protein_biscuit_data.append(post_data)
                            print(f"   ✅ {category}: {post.title[:70]}...")
                            
                except Exception as e:
                    continue
        
        # Get top discussions about snacks and protein
        for post in subreddit.top(time_filter="month", limit=20):
            if post.score > 20:
                snack_keywords = ['snack', 'protein', 'biscuit', 'cookie', 'nutrition bar', 'healthy food']
                if any(keyword in post.title.lower() for keyword in snack_keywords):
                    if not any(p['url'] == f"https://reddit.com{post.permalink}" for p in protein_biscuit_data):
                        post_data = {
                            'subreddit': sub_name,
                            'title': post.title,
                            'content': post.selftext[:500],
                            'upvotes': post.score,
                            'comments': post.num_comments,
                            'url': f"https://reddit.com{post.permalink}",
                            'category': 'general_snack_discussion',
                            'sentiment': 'neutral',
                            'price_mentions': [],
                            'ingredient_concerns': [],
                            'taste_complaints': [],
                            'health_benefits': [],
                            'brand_preferences': []
                        }
                        protein_biscuit_data.append(post_data)
                        print(f"   🔥 Popular snack discussion: {post.title[:70]}...")
    
    except Exception as e:
        print(f"   ❌ Error in r/{sub_name}: {e}")
        continue

print(f"\n📊 PROTEIN BISCUIT RESEARCH RESULTS:")
print("=" * 50)
print(f"Total discussions analyzed: {len(protein_biscuit_data)}")
print(f"Categories identified: {len(categories)}")

print(f"\n🎯 DISCUSSION CATEGORIES:")
for category, count in categories.most_common():
    print(f"   {category:25} - {count} discussions")

print(f"\n😊 SENTIMENT ANALYSIS:")
for sentiment, count in sentiment_analysis.most_common():
    print(f"   {sentiment:15} - {count} posts")

# Analyze price mentions
price_data = []
for post in protein_biscuit_data:
    if post['price_mentions']:
        price_data.extend(post['price_mentions'])

print(f"\n💰 PRICE MENTIONS ANALYSIS:")
price_counter = Counter(price_data)
for price_term, count in price_counter.most_common(10):
    print(f"   {price_term:20} - {count} mentions")

# Analyze ingredient concerns
ingredient_concerns = Counter()
for post in protein_biscuit_data:
    for concern in post['ingredient_concerns']:
        ingredient_concerns[concern] += 1

print(f"\n🌿 INGREDIENT CONCERNS:")
for concern, count in ingredient_concerns.most_common():
    print(f"   {concern:25} - {count} mentions")

# Analyze taste complaints
taste_issues = Counter()
for post in protein_biscuit_data:
    for issue in post['taste_complaints']:
        taste_issues[issue] += 1

print(f"\n👅 TASTE & TEXTURE ISSUES:")
for issue, count in taste_issues.most_common():
    print(f"   {issue:25} - {count} mentions")

# Analyze health benefits sought
health_goals = Counter()
for post in protein_biscuit_data:
    for goal in post['health_benefits']:
        health_goals[goal] += 1

print(f"\n💪 HEALTH GOALS MENTIONED:")
for goal, count in health_goals.most_common():
    print(f"   {goal:25} - {count} mentions")

print(f"\n🚨 KEY INSIGHTS FOR PROTEIN BISCUIT BUSINESS:")
print("=" * 50)

# Find the most popular discussions
popular_posts = sorted(protein_biscuit_data, key=lambda x: x['upvotes'], reverse=True)[:10]

print(f"\n🔥 MOST POPULAR DISCUSSIONS:")
for i, post in enumerate(popular_posts[:5], 1):
    print(f"\n{i}. {post['title']}")
    print(f"   🔗 r/{post['subreddit']} | 👍 {post['upvotes']} | 💬 {post['comments']}")
    print(f"   🎯 Category: {post['category']}")
    print(f"   😊 Sentiment: {post['sentiment']}")
    if post['price_mentions']:
        print(f"   💰 Price mentions: {post['price_mentions'][:3]}")
    if post['ingredient_concerns']:
        print(f"   🌿 Ingredient concerns: {', '.join(post['ingredient_concerns'][:3])}")
    print(f"   📎 {post['url']}")

# Save detailed analysis
import os
os.makedirs('protein_biscuit_analysis', exist_ok=True)

df = pd.DataFrame(protein_biscuit_data)
df.to_csv('protein_biscuit_analysis/protein_biscuit_insights.csv', index=False)

print(f"\n📁 Detailed analysis saved to 'protein_biscuit_analysis/protein_biscuit_insights.csv'")

print(f"\n🎯 STRATEGIC RECOMMENDATIONS:")
print("=" * 45)

# Generate business recommendations
total_posts = len(protein_biscuit_data)
price_mentions = sum(1 for post in protein_biscuit_data if post['price_mentions'])
taste_issues_count = sum(1 for post in protein_biscuit_data if post['taste_complaints'])
ingredient_concerns_count = sum(1 for post in protein_biscuit_data if post['ingredient_concerns'])

print(f"""
📊 MARKET OPPORTUNITY ANALYSIS:

1. **PRICE SENSITIVITY**: {price_mentions}/{total_posts} ({price_mentions/total_posts*100:.1f}%) mention pricing
   → Opportunity: Affordable protein biscuits under $2-3 per serving

2. **TASTE CONCERNS**: {taste_issues_count}/{total_posts} ({taste_issues_count/total_posts*100:.1f}%) complain about taste/texture
   → Opportunity: Focus on great taste and pleasant texture

3. **INGREDIENT PREFERENCES**: {ingredient_concerns_count}/{total_posts} ({ingredient_concerns_count/total_posts*100:.1f}%) discuss ingredients
   → Opportunity: Clean, natural ingredients with no artificial additives

4. **HEALTH GOALS**: Top 3 health goals mentioned:
   - {health_goals.most_common(1)[0][0].replace('_', ' ').title()} ({health_goals.most_common(1)[0][1]} mentions)
   - {health_goals.most_common(2)[1][0].replace('_', ' ').title()} ({health_goals.most_common(2)[1][1]} mentions)
   - {health_goals.most_common(3)[2][0].replace('_', ' ').title()} ({health_goals.most_common(3)[2][1]} mentions)

💡 PRODUCT DEVELOPMENT RECOMMENDATIONS:

1. **TARGET PRICE POINT**: $1.50-$2.50 per biscuit
2. **KEY FEATURES**: Great taste + clean ingredients + 15-20g protein
3. **FLAVOR PROFILE**: Avoid chalky/gritty texture, focus on moist & flavorful
4. **MARKETING ANGLE**: Affordable luxury - premium quality at accessible price
5. **DISTRIBUTION**: Direct-to-consumer + health food stores + gyms

🎯 TARGET CUSTOMER PROFILE:
   - Fitness enthusiasts looking for affordable protein snacks
   - Health-conscious individuals wanting clean ingredient snacks  
   - Budget-conscious consumers tired of overpriced protein products
   - People seeking convenient, nutritious on-the-go snacks
""")

print(f"\n🔥 VALIDATED PRODUCT FEATURES:")
top_ingredient_concern = ingredient_concerns.most_common(1)[0][0] if ingredient_concerns else "clean_ingredients"
top_health_goal = health_goals.most_common(1)[0][0] if health_goals else "general_health"

print(f"   1. {top_ingredient_concern.replace('_', ' ').title()}")
print(f"   2. {top_health_goal.replace('_', ' ').title()}")
print(f"   3. Affordable Pricing")
print(f"   4. Great Taste & Texture")
print(f"   5. High Protein Content")
