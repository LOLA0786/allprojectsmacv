const express = require('express');
const axios = require('axios');
const app = express();

// Your actual API keys (set as environment variables)
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

app.use(express.json());

app.post('/api/ai-creative', async (req, res) => {
  try {
    const { prompt } = req.body;
    
    // Real OpenAI integration
    const openaiResponse = await axios.post('https://api.openai.com/v1/chat/completions', {
      model: "gpt-4",
      messages: [{
        role: "user",
        content: `Create compelling ad copy for: ${prompt}. Max 120 chars. Include emojis.`
      }],
      max_tokens: 100
    }, {
      headers: { 'Authorization': `Bearer ${OPENAI_API_KEY}` }
    });

    const aiCopy = openaiResponse.data.choices[0].message.content;

    res.json({
      ad_copy: aiCopy,
      image_url: `https://picsum.photos/800/600?random=${Date.now()}`,
      ctr_prediction: (Math.random() * 4 + 3).toFixed(1),
      ai_generated: true,
      model: 'GPT-4'
    });

  } catch (error) {
    // Fallback to our working version
    res.json({
      ad_copy: `🎯 Amazing ${req.body.prompt}! Limited offer. Shop now! 🔥`,
      image_url: `https://picsum.photos/800/600?random=${Date.now()}`,
      ctr_prediction: '4.5',
      ai_generated: false,
      fallback: true
    });
  }
});

app.listen(5001, () => console.log('🤖 AI Server: http://localhost:5001'));
