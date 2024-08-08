import React from 'react';
import Banner from './../Home/Banner';
import ChatInterface from './ChatInterface';
import './styles/Chatbot.css';

const Chatbot = () => {
  return (
    <div className="chatbot-page">
      <Banner />
      <main className="chatbot-main">
        <h1>LexCelerate AI Assistant</h1>
        <p>Ask about legal precedents and get instant answers</p>
        <ChatInterface />
      </main>
    </div>
  );
};

export default Chatbot;