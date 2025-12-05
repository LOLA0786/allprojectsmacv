module.exports = {
  score: (creative, context) => {
    return {
      overall_score: Math.floor(Math.random() * 30 + 70),
      engagement_potential: Math.floor(Math.random() * 40 + 30) + '%',
      conversion_likelihood: Math.floor(Math.random() * 35 + 15) + '%',
      viral_probability: Math.floor(Math.random() * 20 + 5) + '%',
      improvement_suggestions: [
        'Add stronger call-to-action',
        'Improve visual hierarchy',
        'Test different color schemes'
      ]
    };
  }
};
