const express = require('express');
const path    = require('path');
const app     = express();

app.use(express.json());
app.use(express.static('public'));

console.log('🎯 MartechOS Pro – root static fix');

// ---------- 8 API endpoints ----------
app.post('/api/predict-performance', (req, res) => {
  res.json({
    success: true,
    prediction: {
      success_probability: 85,
      expected_roi: '350%',
      confidence: 92,
      platforms: ['Instagram', 'TikTok', 'YouTube'],
      risk_factors: ['Audience saturation', 'Seasonal trends']
    }
  });
});

app.post('/api/generate-video', (req, res) => {
  res.json({
    success: true,
    video: {
      video_id: 'vid_' + Date.now(),
      duration: '30s',
      ai_avatar: 'digital_influencer_1',
      voice_clone: 'professional_male',
      background_score: 'upbeat_corporate',
      subtitles: true,
      estimated_time: '2 minutes'
    }
  });
});

app.post('/api/generate-creatives', (req, res) => {
  const { product } = req.body;
  if (!product) return res.status(400).json({ success: false, message: 'Product is required' });
  const creatives = [
    { type: 'UGC Video Ad',   conversion_rate: '15%', ctr: '4.8%', best_performance: { location: 'Mumbai', day: 'Friday', time: '7-9 PM' }, platforms: ['Instagram', 'TikTok'], estimated_engagement: '15-25%' },
    { type: 'Carousel Post',  conversion_rate: '12%', ctr: '3.9%', best_performance: { location: 'Delhi',  day: 'Wednesday', time: '12-2 PM' }, platforms: ['Instagram', 'Facebook'], estimated_engagement: '12-18%' },
    { type: 'Story Ad',       conversion_rate: '18%', ctr: '5.2%', best_performance: { location: 'Bangalore', day: 'Saturday', time: '6-8 PM' }, platforms: ['Instagram', 'Snapchat'], estimated_engagement: '18-28%' },
    { type: 'AR Filter Ad',   conversion_rate: '22%', ctr: '5.9%', best_performance: { location: 'Metro Cities', day: 'Friday', time: '6-9 PM' }, platforms: ['Instagram', 'Snapchat'], estimated_engagement: '25-40%' }
  ];
  res.json({ success: true, product, creative_analytics: creatives, total_creatives: creatives.length, ai_recommendation: creatives[0] });
});

app.post('/api/generate-ugc', (req, res) => {
  res.json({
    success: true,
    ugc_kits: [
      { type: 'Testimonial Template', duration: '30-60 seconds', platforms: ['Instagram', 'TikTok'], script: 'Share your real experience with our product!', hashtags: ['#review', '#testimonial', '#ugc'] },
      { type: 'Tutorial Template',    duration: '45-90 seconds', platforms: ['YouTube', 'Instagram'], script: 'Step-by-step guide to using our product', hashtags: ['#tutorial', '#howto', '#guide'] }
    ]
  });
});

app.post('/api/generate-cgi', (req, res) => {
  res.json({
    success: true,
    cgi_overlays: [
      { type: '3D Product View',  format: 'AR/3D',     platforms: ['Instagram', 'Snapchat'], features: ['360° view', 'Interactive', 'Realistic'] },
      { type: 'Motion Graphics',  format: 'Video Overlay', platforms: ['All Platforms'],      features: ['Animated text', 'Visual effects', 'Brand elements'] }
    ]
  });
});

app.get('/api/platform-comparison', (req, res) => {
  res.json({
    success: true,
    platforms: [
      { platform: 'Instagram', avg_ctr: '4.8%', conversion_rate: '3.8%', cost_per_click: '₹45', best_for: 'Visual products, fashion, lifestyle' },
      { platform: 'TikTok',    avg_ctr: '5.2%', conversion_rate: '4.1%', cost_per_click: '₹38', best_for: 'Young audience, viral content' }
    ],
    top_recommendation: 'TikTok for highest CTR'
  });
});

app.post('/api/analyze-keywords', (req, res) => {
  const { product } = req.body;
  if (!product) return res.status(400).json({ success: false, message: 'Product is required' });
  res.json({
    success: true,
    keywords: [
      { keyword: `buy ${product}`,      ctr: '5.2%', volume: 45000 },
      { keyword: `${product} price`,    ctr: '4.3%', volume: 55000 },
      { keyword: `best ${product}`,     ctr: '5.2%', volume: 45000 },
      { keyword: `${product} online`,   ctr: '4.8%', volume: 32000 }
    ],
    top_keyword: `buy ${product}`
  });
});

app.post('/api/send-otp',    (req, res) => res.json({ success: true, message: 'OTP sent',     method: req.body.email ? 'email' : 'sms', otp_code: '123456' }));
app.post('/api/verify-otp',  (req, res) => res.json({ success: true, message: 'OTP verified', user_token: 'user_' + Date.now(), user_profile: { name: 'Demo User', email: req.body.email, plan: 'premium' } }));
app.get('/api/status',       (req, res) => res.json({ success: true, status: 'operational', version: '4.0.0', features: ['predict-performance','generate-video','generate-creatives','generate-ugc','generate-cgi','platform-comparison','analyze-keywords','otp-login'] }));

// ---------- serve front-end ----------
app.get('/', (req, res) => res.sendFile(path.resolve(__dirname, 'public', 'index.html')));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ ALL ENDPOINTS + static root on port ${PORT}`));
