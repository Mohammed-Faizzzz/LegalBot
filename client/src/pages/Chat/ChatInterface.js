import React, { useState } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { text: "Welcome to LexCelerate AI Assistant. How can I help you today?", isUser: false }
  ]);

  const handleSendMessage = (message) => {
    setMessages([...messages, { text: message, isUser: true }]);
    
    // Simulate AI response (replace with actual API call)
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        text: "I'm processing your request about legal precedents. Please allow me a moment to search our database.", 
        isUser: false 
      }]);
    }, 1000);
  };

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        {messages.map((message, index) => (
          <ChatMessage key={index} message={message} />
        ))}
      </div>
      <ChatInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatInterface;