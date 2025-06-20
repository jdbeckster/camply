import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import NotificationForm from './pages/NotificationForm';
import NotificationList from './pages/NotificationList';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main className="container">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/create-notification" element={<NotificationForm />} />
            <Route path="/notifications" element={<NotificationList />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 