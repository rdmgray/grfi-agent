import React from 'react';
import './Message.css';

const Message = ({ message }) => {
  const { type, text, timestamp, isError } = message;

  const formatTime = (date) => {
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className={`message ${type} ${isError ? 'error' : ''}`}>
      <div className="message-content">
        {type === 'agent' && (
          <div className="message-avatar">
            <img src="/images/liana_logo.svg" alt="Liana" className="avatar-icon" />
          </div>
        )}
        <div className="message-bubble">
          <div className="message-text">{text}</div>
          <div className="message-time">{formatTime(timestamp)}</div>
        </div>
        {type === 'user' && (
          <div className="message-avatar user-avatar">
            <span className="avatar-icon">👤</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default Message;
