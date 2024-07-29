import React from 'react';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import './styles/FeaturesSection.css';

const FeaturesSection = () => {
  return (
    <section id="features">
      <h1>Tired of spending hours on legal research? There's a better way.</h1>
      <p className='tagline'> We recognized the frustration legal professionals face when searching through countless documents for relevant precedents. That's why we created LexCelerate. Our AI-powered platform streamlines legal research, allowing lawyers to focus on building winning arguments instead of getting lost in document stacks. By collaborating with legal experts, we've developed a tool that accelerates research, bringing powerful insights to light faster and transforming how legal professionals work. </p>
      <div className="features-container">
        <div className="column without-buildkwik">
          <h3 style={{color:"#a30000"}}>Without BuildKwik</h3>
          <ul>
            <li><CancelIcon className="list-icon" /> Manual searching through case law</li>
            <li><CancelIcon className="list-icon" /> Time-consuming document review</li>
            <li><CancelIcon className="list-icon" /> Risk of overlooking relevant precedents</li>
            <li><CancelIcon className="list-icon" /> Inconsistent research results</li>
            <li><CancelIcon className="list-icon" /> Limited access to comprehensive databases</li>
            <li><CancelIcon className="list-icon" /> Challenges in cross-referencing multiple sources</li>
          </ul>
        </div>
        <div className="column with-buildkwik">
          <h3 style={{color:"#006400"}}>With BuildKwik</h3>
          <ul>
            <li><CheckCircleIcon className="icon" /> AI-powered rapid case law search</li>
            <li><CheckCircleIcon className="icon" /> Efficient document analysis</li>
            <li><CheckCircleIcon className="icon" /> Comprehensive precedent discovery</li>
            <li><CheckCircleIcon className="icon" /> Consistent, reliable results</li>
            <li><CheckCircleIcon className="icon" /> Access to vast legal databases</li>
            <li><CheckCircleIcon className="icon" /> Seamless cross-referencing of sources</li>
          </ul>
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
