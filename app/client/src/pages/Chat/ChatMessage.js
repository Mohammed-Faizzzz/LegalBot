import React from 'react';

const ChatMessage = ({ message }) => {
  return (
    <div className={`chat-message ${message.isUser ? 'user' : 'ai'}`}>
      <div className="message-content">{message.text}</div>
    </div>
  );
};

export default ChatMessage;