import React, { useState } from 'react';
import './MessageInput.css';

const MessageInput = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message);
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form className="message-input-container" onSubmit={handleSubmit}>
      <div className="input-wrapper">
        <input
          type="text"
          className="message-input"
          placeholder="Ask about sustainability data, ESG metrics, impact investing..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
        />
        <button
          type="submit"
          className="send-button"
          disabled={!message.trim() || isLoading}
        >
          <span className="send-icon">📤</span>
        </button>
      </div>
    </form>
  );
};

export default MessageInput;
