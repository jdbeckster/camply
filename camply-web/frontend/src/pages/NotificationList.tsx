import React, { useState, useEffect } from 'react';
import { getNotifications, deleteNotification, testNotification } from '../api/notifications';

interface Notification {
  id: number;
  recreation_area_name?: string;
  campground_name?: string;
  campsite_name?: string;
  start_date: string;
  end_date: string;
  phone_number: string;
  is_active: boolean;
  created_at: string;
}

const NotificationList: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    loadNotifications();
  }, []);

  const loadNotifications = async () => {
    try {
      const data = await getNotifications();
      setNotifications(data);
    } catch (err: any) {
      setError('Failed to load notifications. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this alert?')) {
      return;
    }

    try {
      await deleteNotification(id);
      setSuccess('Alert deleted successfully.');
      loadNotifications(); // Reload the list
    } catch (err: any) {
      setError('Failed to delete alert. Please try again.');
    }
  };

  const handleTestNotification = async (id: number) => {
    try {
      await testNotification(id);
      setSuccess('Test notification sent successfully!');
    } catch (err: any) {
      setError('Failed to send test notification. Please try again.');
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getLocationDescription = (notification: Notification) => {
    if (notification.campsite_name) {
      return `${notification.campsite_name} in ${notification.campground_name}`;
    } else if (notification.campground_name) {
      return notification.campground_name;
    } else if (notification.recreation_area_name) {
      return notification.recreation_area_name;
    }
    return 'Any available location';
  };

  if (loading) {
    return <div className="loading">Loading your alerts...</div>;
  }

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h1 className="card-title">My Campsite Alerts</h1>
        </div>

        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        {notifications.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
            <p>You don't have any alerts yet.</p>
            <a href="/create-notification" className="btn btn-primary">
              Create Your First Alert
            </a>
          </div>
        ) : (
          <div>
            {notifications.map((notification) => (
              <div key={notification.id} className="card" style={{ marginBottom: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div style={{ flex: 1 }}>
                    <h3 style={{ margin: '0 0 0.5rem 0', color: '#333' }}>
                      {getLocationDescription(notification)}
                    </h3>
                    
                    <div style={{ color: '#666', marginBottom: '0.5rem' }}>
                      <strong>Dates:</strong> {formatDate(notification.start_date)} - {formatDate(notification.end_date)}
                    </div>
                    
                    <div style={{ color: '#666', marginBottom: '0.5rem' }}>
                      <strong>Phone:</strong> {notification.phone_number}
                    </div>
                    
                    <div style={{ color: '#666', marginBottom: '0.5rem' }}>
                      <strong>Status:</strong> 
                      <span style={{ 
                        color: notification.is_active ? '#28a745' : '#dc3545',
                        fontWeight: 'bold',
                        marginLeft: '0.5rem'
                      }}>
                        {notification.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                    
                    <div style={{ color: '#999', fontSize: '0.9rem' }}>
                      Created: {formatDate(notification.created_at)}
                    </div>
                  </div>
                  
                  <div style={{ display: 'flex', gap: '0.5rem', flexDirection: 'column' }}>
                    <button
                      onClick={() => handleTestNotification(notification.id)}
                      className="btn btn-secondary"
                      style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}
                    >
                      Test Alert
                    </button>
                    
                    <button
                      onClick={() => handleDelete(notification.id)}
                      className="btn btn-danger"
                      style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default NotificationList; 