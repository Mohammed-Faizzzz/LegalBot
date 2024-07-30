import React, { useState } from 'react';

const ChatInput = ({ onSendMessage }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSendMessage(input);
      setInput('');
    }
  };

  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask about legal precedents..."
      />
      <button type="submit">Send</button>
    </form>
  );
};

export default ChatInput;