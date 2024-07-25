import React from 'react';
import './styles/TestimonialsSection.css';

const TestimonialsSection = () => {
  return (
    <section id="testimonials">
      <h2>Hear From Our Clients</h2>
      <div className="testimonials-container">
        <div className="testimonial">
          <p>"BuildKwik has transformed our business! The user-friendly interface and seamless integration with our existing systems have made our operations much more efficient."</p>
          <h4>- Alex P.</h4>
        </div>
        <div className="testimonial">
          <p>"A game-changer in the industry. The AI-powered features have significantly improved our customer interactions and overall satisfaction."</p>
          <h4>- Jamie L.</h4>
        </div>
        <div className="testimonial">
          <p>"Exceptional service and support. The BuildKwik team has been incredibly responsive and helpful in addressing our needs and questions."</p>
          <h4>- Morgan R.</h4>
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;
