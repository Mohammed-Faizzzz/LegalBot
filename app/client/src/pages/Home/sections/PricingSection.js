import React from 'react';
import './styles/PricingSection.css';

const PricingSection = () => {
  return (
    <section id="pricing">
      <h2>Choose Your LexCelerate Plan</h2>
      <p className='tagline'>Accelerate Your Legal Research with the Right Subscription</p>
      <div className="pricing-container">
        <div className="pricing-plan individual">
          <h3>Individual</h3>
          <div className="price">
            <span className="amount">$99</span>
            <span className="period">/month</span>
          </div>
          <ul>
            <li>AI-powered case law search</li>
            <li>Document analysis</li>
            <li>Access to legal databases</li>
            <li>Basic support</li>
          </ul>
          <button>Start Free Trial</button>
        </div>
        <div className="pricing-plan team featured">
          <div className="featured-label">Most Popular</div>
          <h3>Team</h3>
          <div className="price">
            <span className="amount">$249</span>
            <span className="period">/month</span>
          </div>
          <ul>
            <li>All Individual features</li>
            <li>Team collaboration tools</li>
            <li>Advanced analytics</li>
            <li>Priority support</li>
            <li>Up to 10 users</li>
          </ul>
          <button>Start Free Trial</button>
        </div>
        <div className="pricing-plan enterprise">
          <h3>Enterprise</h3>
          <div className="price">
            <span className="amount">Custom</span>
          </div>
          <ul>
            <li>All Team features</li>
            <li>Custom integrations</li>
            <li>Dedicated account manager</li>
            <li>24/7 premium support</li>
            <li>Unlimited users</li>
          </ul>
          <button>Contact Sales</button>
        </div>
      </div>
    </section>
  );
};

export default PricingSection;