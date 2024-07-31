const express = require('express');
const router = express.Router();
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

// @route  POST api/stripe/payment
// @desc   Process payment
// @access Private
router.post('/payment', async (req, res) => {
  const { amount, token } = req.body;
  try {
    const charge = await stripe.charges.create({
      amount,
      currency: 'usd',
      description: 'Boilerplate Purchase',
      source: token.id,
    });
    res.json(charge);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server error');
  }
});

module.exports = router;
