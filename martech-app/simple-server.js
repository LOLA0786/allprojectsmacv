const express = require('express');
const app = express();

app.use(express.json());

app.post('/api/generate-creative', (req, res) => {
  console.log('Received:', req.body);
  res.json({
    success: true,
    ad_copy: `🎉 Amazing ${req.body.prompt}! Limited time offer. Shop now!`,
    image_url: 'https://picsum.photos/600/400',
    ctr_prediction: '4.5'
  });
});

app.get('/api/status', (req, res) => {
  res.json({ status: 'OK', message: 'Server is working!' });
});

app.listen(5000, () => {
  console.log('✅ Simple server running on http://localhost:5000');
});
