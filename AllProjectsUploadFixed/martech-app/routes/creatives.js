const express = require('express');
const router = express.Router();

router.post('/generate', (req, res) => {
  res.json({ message: 'Creatives endpoint working!' });
});

module.exports = router;
