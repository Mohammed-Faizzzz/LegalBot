import React from 'react';
import './styles/HeroSection.css';

const HeroSection = () => {
  return (
    <section id="hero">
      <div className="hero-main">
        <div className="hero-content">
          <h1>Build Faster, Launch Sooner</h1>
          <p>Accelerate your development process and bring your ideas to life faster than ever!</p>
          <button>Get BuildKwik</button>
        </div>
      </div>
      <div className="hero-side">
        <div className="user-guide">
          <h2>How It Works</h2>
          <ol>
            <li><strong>Sign Up:</strong> Create an account in minutes.</li>
            <li><strong>Choose a Plan:</strong> Select the plan that fits your needs.</li>
            <li><strong>Start Building:</strong> Use our tools to develop your app quickly.</li>
            <li><strong>Launch:</strong> Deploy your app with ease and start growing.</li>
          </ol>
        </div>
        <div className="divider"></div>
        <div className="testimonials">
          <h2 style={{textAlign: "center"}}>Hear From Our Clients</h2>
          <p>"BuildKwik has transformed our business! The user-friendly interface and seamless integration with our existing systems have made our operations much more efficient."</p>
          <h4>- Alex P.</h4>
          {/* <p>"A game-changer in the industry. The AI-powered features have significantly improved our customer interactions and overall satisfaction."</p>
          <h4>- Jamie L.</h4> */}
          <p>"Exceptional service and support. The BuildKwik team has been incredibly responsive and helpful in addressing our needs and questions."</p>
          <h4>- Morgan R.</h4>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
