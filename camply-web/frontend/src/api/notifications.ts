import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface NotificationData {
  recreation_area_id?: number;
  recreation_area_name?: string;
  campground_id?: number;
  campground_name?: string;
  campsite_id?: number;
  campsite_name?: string;
  start_date: string;
  end_date: string;
  phone_number: string;
}

export interface Notification {
  id: number;
  user_id: number;
  recreation_area_id?: number;
  recreation_area_name?: string;
  campground_id?: number;
  campground_name?: string;
  campsite_id?: number;
  campsite_name?: string;
  start_date: string;
  end_date: string;
  phone_number: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export const createNotification = async (data: NotificationData): Promise<Notification> => {
  const response = await axios.post(`${API_BASE_URL}/api/notifications/`, data);
  return response.data;
};

export const getNotifications = async (): Promise<Notification[]> => {
  const response = await axios.get(`${API_BASE_URL}/api/notifications/`);
  return response.data;
};

export const getNotification = async (id: number): Promise<Notification> => {
  const response = await axios.get(`${API_BASE_URL}/api/notifications/${id}`);
  return response.data;
};

export const updateNotification = async (id: number, data: Partial<NotificationData>): Promise<Notification> => {
  const response = await axios.put(`${API_BASE_URL}/api/notifications/${id}`, data);
  return response.data;
};

export const deleteNotification = async (id: number): Promise<void> => {
  await axios.delete(`${API_BASE_URL}/api/notifications/${id}`);
};

export const testNotification = async (id: number): Promise<void> => {
  await axios.post(`${API_BASE_URL}/api/notifications/${id}/test`);
};

export const getNotificationHistory = async (id: number, limit: number = 50): Promise<any[]> => {
  const response = await axios.get(`${API_BASE_URL}/api/notifications/${id}/history?limit=${limit}`);
  return response.data;
}; 