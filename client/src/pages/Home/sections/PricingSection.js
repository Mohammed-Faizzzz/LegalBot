import React from 'react';
import './styles/PricingSection.css';

const PricingSection = () => {
  return (
    <section id="pricing">
      <h2>Discover Our Pricing Plans</h2>
      <p className='tagline'> Find the Perfect Plan for Your Needs</p>
      <div className="pricing-container">
        <div className="pricing-plan">
          {/* <h3>Basic</h3> */}
          <div className="price">
            <h1>$5</h1><p>SGD</p>
          </div>
          <ul>
            <li>Access to basic components</li>
            <li>Standard support</li>
            <li>Single user license</li>
          </ul>
          <button>Choose Plan</button>
        </div>
        <div className="pricing-plan">
          {/* <h3>Standard</h3> */}
          <div className="price">
            <h1>$10</h1><p>SGD</p>
          </div>
          <ul>
            <li>Access to all components</li>
            <li>Priority support</li>
            <li>Team license (up to 5 users)</li>
            <li>Regular updates</li>
          </ul>
          <button>Choose Plan</button>
        </div>
        <div className="pricing-plan">
          {/* <h3>Premium</h3> */}
          <div className="price">
            <h1>$20</h1><p>SGD</p>
          </div>
          <ul>
            <li>Access to all components</li>
            <li>24/7 Premium support</li>
            <li>Enterprise license (unlimited users)</li>
            <li>Regular updates</li>
            <li>Access to exclusive features</li>
          </ul>
          <button>Choose Plan</button>
        </div>
      </div>
    </section>
  );
};

export default PricingSection;
