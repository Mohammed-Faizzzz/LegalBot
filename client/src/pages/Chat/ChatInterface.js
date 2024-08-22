import React, { useState } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { text: "Welcome to LexCelerate AI Assistant. How can I help you today?", isUser: false }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const API_URL = 'api/query';

  const handleSendMessage = async (message) => {
    setMessages(prev => [...prev, { text: message, isUser: true }]);
    setIsLoading(true);
    setMessages(prev => [...prev, { text: "Loading...", isUser: false, isLoading: true }]);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: message }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const data = await response.json();

        setMessages(prev => [
          ...prev.slice(0, -1), // Remove the loading message
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
      setMessages(prev => [
        ...prev.slice(0, -1), // Remove the loading message
        {
          text: 'Sorry, there was an error processing your request.',
          isUser: false,
        },
      ]);
    } finally {
      setIsLoading(false);
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