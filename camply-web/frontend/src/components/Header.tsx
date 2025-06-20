import React from 'react';
import { Link } from 'react-router-dom';

const Header: React.FC = () => {
  return (
    <header style={{
      background: 'white',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      padding: '1rem 0',
      marginBottom: '2rem'
    }}>
      <div className="container">
        <nav style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <Link to="/" style={{
            textDecoration: 'none',
            color: '#333',
            fontSize: '1.5rem',
            fontWeight: 'bold'
          }}>
            ⛺️ Camply Web Interface
          </Link>
          
          <div style={{ display: 'flex', gap: '1rem' }}>
            <Link to="/" className="btn btn-secondary">
              Home
            </Link>
            <Link to="/create-notification" className="btn btn-primary">
              Create Alert
            </Link>
            <Link to="/notifications" className="btn btn-secondary">
              My Alerts
            </Link>
          </div>
        </nav>
      </div>
    </header>
  );
};

export default Header; 