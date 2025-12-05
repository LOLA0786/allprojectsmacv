const express = require('express');
const router = express.Router();

router.post('/location-insights', (req, res) => {
  const { brandLocation, industry } = req.body;
  
  // White River Media specific analytics
  const insights = {
    top_cities: [
      { city: "Mumbai", performance: "92%", reasoning: "Financial capital advantage" },
      { city: "Bangalore", performance: "88%", reasoning: "Tech hub engagement" }
    ],
    recommendations: [
      `Focus 40% budget on ${brandLocation} for local impact`,
      "Leverage your media industry expertise"
    ]
  };
  
  res.json(insights);
});

module.exports = router;
