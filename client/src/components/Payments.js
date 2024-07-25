import React from 'react';
import StripeCheckout from 'react-stripe-checkout';
import axios from 'axios';

const Payment = ({ amount }) => {
  const onToken = async (token) => {
    const res = await axios.post('/api/stripe/payment', { token, amount });
    console.log(res.data);
  };

  return (
    <StripeCheckout
      token={onToken}
      stripeKey="your-publishable-key"
      amount={amount}
      name="Boilerplate Purchase"
      description="Purchase a boilerplate template"
    />
  );
};

export default Payment;
