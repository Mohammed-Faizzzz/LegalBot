import React from 'react';

const ChatMessage = ({ message }) => {
  return (
    <div className={`chat-message ${message.isUser ? 'user' : 'ai'}`}>
      <div className="message-content">
        {message.isLoading ? (
          <span className="loading">Loading...</span>
        ) : (
          message.text
        )}
      </div>
    </div>
  );
};

export default ChatMessage;