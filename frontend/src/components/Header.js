import React from 'react';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo-section">
          <div className="logo-icon">
            <img src="/images/liana_logo.svg" alt="Liana Logo" />
          </div>
          <div className="logo-text">
            <h1>Liana</h1>
            <p className="subtitle">Sustainability & Impact Data Intelligence</p>
          </div>
        </div>
        <div className="header-badge">
          <span className="badge">Prototype</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
