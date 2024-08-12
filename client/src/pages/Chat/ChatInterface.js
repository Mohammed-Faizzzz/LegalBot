import React, { useState } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { text: "Welcome to LexCelerate AI Assistant. How can I help you today?", isUser: false }
  ]);

  const API_URL = 'api/query';

  const handleSendMessage = async (message) => {
    setMessages([...messages, { text: message, isUser: true }]);
  
    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: message }),
      });
  
      // Check if the response is JSON
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const data = await response.json();
  
        setMessages((prev) => [
          ...prev,
          {
            text: data.predicted_answer,
            isUser: false,
            confidence: data.confidence,
          },
        ]);
      } else {
        throw new Error('Response was not JSON');
      }
    } catch (error) {
      console.error('Error:', error.message);
      setMessages((prev) => [
        ...prev,
        {
          text: 'Sorry, there was an error processing your request.',
          isUser: false,
        },
      ]);
    }
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