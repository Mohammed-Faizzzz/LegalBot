import React from 'react';
import './App.css';
import Banner from './pages/Home/Banner';
import Footer from './pages/Home/Footer';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Signup from './pages/Auth/Signup';
import Login from './pages/Auth/Login';

import HeroSection from './pages/Home/sections/HeroSection';
import FeaturesSection from './pages/Home/sections/FeaturesSection';
import PricingSection from './pages/Home/sections/PricingSection';
import TestimonialsSection from './pages/Home/sections/TestimonialsSection';
import ContactSection from './pages/Home/sections/ContactSection';
import FutureSection from './pages/Home/sections/FutureSection';

const Home = () => (
  <div className="App">
    <div className="App-body">
      <Banner />
      <HeroSection />
      <FeaturesSection />
      <PricingSection />
      <FutureSection />
      {/* <TestimonialsSection /> */}
      {/* <ContactSection /> */}
    </div>
    <Footer />
  </div>
);

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </Router>
  );
}

export default App;
