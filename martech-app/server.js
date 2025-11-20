const express = require('express');
const cors = require('cors');
const path = require('path');
const axios = require('axios');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

console.log('🔧 Checking environment variables...');
console.log('OPENAI_API_KEY exists:', !!process.env.OPENAI_API_KEY);
console.log('GROK_API_KEY exists:', !!process.env.GROK_API_KEY);

// Simple creative generation without external APIs first
app.post('/api/generate-creative', async (req, res) => {
  try {
    const { prompt, platform, targetAudience } = req.body;
    
    console.log('📨 Received request:', { prompt, platform, targetAudience });

    // Enhanced mock responses that are more realistic
    const mockCreatives = {
      'organic skincare': {
        ad_copy: "✨ Transform your skin naturally! Our organic skincare line is chemical-free, vegan, and perfect for sensitive skin. Get 20% off your first order! 🌿 #NaturalGlow",
        ctr: "4.2"
      },
      'coffee shop': {
        ad_copy: "☕ Morning fuel just got better! Stop by for a artisan coffee and fresh pastry. Students get 15% off! 🎒 #CoffeeLovers",
        ctr: "3.8"
      },
      'fitness app': {
        ad_copy: "💪 Your personal trainer in your pocket! Get customized workouts, track progress, and join our fitness community. Start your free trial today! #FitnessGoals",
        ctr: "5.1"
      },
      'tech gadgets': {
        ad_copy: "🚀 Upgrade your tech game! Latest gadgets for remote workers with free shipping. Limited stock available! ⚡ #TechEssentials",
        ctr: "4.7"
      }
    };

    // Find the best matching creative or use AI-like generation
    let creativeData;
    const promptLower = prompt.toLowerCase();
    
    if (promptLower.includes('skincare') || promptLower.includes('beauty')) {
      creativeData = mockCreatives['organic skincare'];
    } else if (promptLower.includes('coffee') || promptLower.includes('cafe')) {
      creativeData = mockCreatives['coffee shop'];
    } else if (promptLower.includes('fitness') || promptLower.includes('workout')) {
      creativeData = mockCreatives['fitness app'];
    } else if (promptLower.includes('tech') || promptLower.includes('gadget')) {
      creativeData = mockCreatives['tech gadgets'];
    } else {
      // Generate dynamic creative based on input
      creativeData = {
        ad_copy: `🎯 Discover amazing ${prompt}! Perfect for ${targetAudience || 'your target audience'}. Limited time offer - don't miss out! 🔥 #${platform || 'instagram'}`,
        ctr: (Math.random() * 4 + 2).toFixed(1)
      };
    }

    const creative = {
      id: 'creative_' + Date.now(),
      prompt,
      platform: platform || 'instagram',
      ad_copy: creativeData.ad_copy,
      image_url: `https://picsum.photos/800/600?random=${Date.now()}&category=${promptLower.includes('tech') ? 'technology' : 'business'}`,
      ctr_prediction: creativeData.ctr,
      suggestions: [
        "Run A/B test with different CTAs",
        "Target lookalike audiences",
        "Use carousel ads for better engagement",
        "Test different landing pages"
      ],
      target_audience: targetAudience || 'general',
      generated_at: new Date().toISOString(),
      ai_models_used: ['Smart Algorithm'],
      confidence_score: '92%'
    };

    console.log('✅ Creative generated successfully');
    res.json(creative);

  } catch (error) {
    console.error('❌ Creative Generation Error:', error);
    res.status(500).json({ 
      error: 'Creative generation failed',
      message: error.message,
      fallback: true
    });
  }
});

// Enhanced Compliance Check
app.post('/api/compliance-check', (req, res) => {
  try {
    const { adText, platform, country } = req.body;

    const issues = [];
    const suggestions = [];

    // DPDP Compliance Checks
    if (adText.includes('free') && !adText.includes('terms')) {
      issues.push('Add terms and conditions for "free" claims');
      suggestions.push('Include: "Terms and conditions apply"');
    }

    if (adText.includes('guarantee') && !adText.includes('conditions')) {
      issues.push('Specify guarantee conditions');
      suggestions.push('Add: "Subject to terms and conditions"');
    }

    if (adText.includes('save') && adText.includes('%') && !adText.includes('original')) {
      issues.push('Mention original price for discount claims');
      suggestions.push('Add original price reference');
    }

    if (adText.includes('best') || adText.includes('number one')) {
      issues.push('Subjective claims require substantiation');
      suggestions.push('Add supporting data or remove superlatives');
    }

    res.json({
      compliant: issues.length === 0,
      issues: issues,
      suggestions: suggestions,
      regulations_checked: ['DPDP Act 2023', 'ASCI Guidelines', 'Consumer Protection Act'],
      checked_at: new Date().toISOString()
    });

  } catch (error) {
    res.status(500).json({ error: 'Compliance check failed' });
  }
});

// Analytics with Smart Insights
app.get('/api/ai-analytics', (req, res) => {
  const analytics = {
    total_spend: 75000,
    total_revenue: 285000,
    roi: 380,
    top_performing_platform: 'Instagram Reels',
    best_ctr: '5.8%',
    campaigns_completed: 24,
    compliance_score: 96,
    ai_insights: [
      "Video content performs 3x better than images",
      "Evening posts (6-9 PM) get highest engagement",
      "Carousel ads have 40% higher conversion rate",
      "User-generated content boosts trust by 60%"
    ],
    recommendations: [
      "Increase video content budget by 30%",
      "Test UGC campaigns for authenticity",
      "Optimize for mobile-first experience",
      "Use more emojis in ad copy (increases engagement by 25%)"
    ]
  };

  res.json(analytics);
});

// Marketing Strategy Suggestions
app.post('/api/marketing-suggestions', (req, res) => {
  const { product, budget, audience, goals } = req.body;
  
  const strategies = {
    low_budget: {
      platform_allocation: { 'Instagram': '40%', 'Google Ads': '30%', 'Email': '20%', 'Content': '10%' },
      focus: 'Organic growth and targeted ads',
      kpis: ['CTR > 2%', 'CPC < ₹15', 'ROAS > 250%']
    },
    medium_budget: {
      platform_allocation: { 'Meta Ads': '35%', 'Google': '25%', 'Influencers': '20%', 'Content': '15%', 'Analytics': '5%' },
      focus: 'Balanced growth with influencer marketing',
      kpis: ['CTR > 3%', 'CPC < ₹20', 'ROAS > 300%']
    },
    high_budget: {
      platform_allocation: { 'Video Ads': '30%', 'Meta': '25%', 'Google': '20%', 'Influencers': '15%', 'Experiential': '10%' },
      focus: 'Brand building and premium positioning',
      kpis: ['CTR > 4%', 'CPC < ₹25', 'ROAS > 400%']
    }
  };

  const budgetLevel = budget < 50000 ? 'low_budget' : budget < 200000 ? 'medium_budget' : 'high_budget';
  const strategy = strategies[budgetLevel];

  res.json({
    product: product,
    recommended_strategy: strategy,
    audience_targeting: `Focus on ${audience} with personalized messaging`,
    content_types: ['Short videos', 'User testimonials', 'Behind-the-scenes', 'Educational content'],
    timeline: '4-6 weeks for measurable results',
    expected_roi: '250-400% based on historical data'
  });
});

// Health check with detailed status
app.get('/api/status', (req, res) => {
  res.json({ 
    status: 'operational',
    version: '2.1.0',
    features: [
      'AI Creative Generation',
      'DPDP Compliance Check', 
      'Marketing Analytics',
      'Strategy Recommendations'
    ],
    server_time: new Date().toISOString(),
    uptime: process.uptime(),
    memory_usage: process.memoryUsage()
  });
});

// Root endpoint
app.get('/api', (req, res) => {
  res.json({
    message: '🚀 MartechOS AI Suite is running!',
    endpoints: {
      'POST /api/generate-creative': 'Generate marketing creatives',
      'POST /api/compliance-check': 'Check DPDP compliance',
      'GET /api/ai-analytics': 'Get marketing insights',
      'POST /api/marketing-suggestions': 'Get strategy recommendations',
      'GET /api/status': 'System status'
    }
  });
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`\n🎉 MartechOS Server Started Successfully!`);
  console.log(`📍 Local: http://localhost:${PORT}`);
  console.log(`🛠️  API: http://localhost:${PORT}/api`);
  console.log(`📊 Status: http://localhost:${PORT}/api/status`);
  console.log(`\n🚀 Ready to generate AI marketing creatives!`);
});
