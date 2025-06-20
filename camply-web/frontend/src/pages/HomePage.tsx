import React from 'react';
import { Link } from 'react-router-dom';

const HomePage: React.FC = () => {
  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h1 className="card-title">Welcome to Camply Web Interface</h1>
        </div>
        <p style={{ fontSize: '1.1rem', lineHeight: '1.6', color: '#666' }}>
          Find and get notified about campsite availability across thousands of campgrounds. 
          Camply searches Recreation.gov, Yellowstone, California State Parks, and many more 
          camping providers to help you secure your perfect camping spot.
        </p>
        
        <div style={{ marginTop: '2rem' }}>
          <Link to="/create-notification" className="btn btn-primary" style={{ marginRight: '1rem' }}>
            Create Your First Alert
          </Link>
          <Link to="/notifications" className="btn btn-secondary">
            View My Alerts
          </Link>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', marginTop: '2rem' }}>
        <div className="card">
          <h3>🔍 Smart Search</h3>
          <p>Search across multiple camping providers including Recreation.gov, Yellowstone, and state parks.</p>
        </div>
        
        <div className="card">
          <h3>📱 Instant Notifications</h3>
          <p>Get SMS alerts when campsites become available so you can book quickly.</p>
        </div>
        
        <div className="card">
          <h3>🎯 Flexible Criteria</h3>
          <p>Set specific date ranges, choose recreation areas, campgrounds, or individual campsites.</p>
        </div>
        
        <div className="card">
          <h3>⚡ Real-time Monitoring</h3>
          <p>Continuous monitoring of availability with instant notifications when spots open up.</p>
        </div>
      </div>

      <div className="card" style={{ marginTop: '2rem' }}>
        <h3>Supported Providers</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
          <div>
            <strong>Recreation.gov</strong>
            <p>US National Parks and Federal Lands</p>
          </div>
          <div>
            <strong>Yellowstone</strong>
            <p>Yellowstone National Park Lodges</p>
          </div>
          <div>
            <strong>ReserveCalifornia</strong>
            <p>California State Parks</p>
          </div>
          <div>
            <strong>GoingToCamp</strong>
            <p>Canadian and US State Parks</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 