import { apiClient } from '@/lib/api';
import { WeatherCurrent, WeatherForecast, NotificationItem, ExpertReview, AdminAnalytics, User } from '@/types';

export const weatherService = {
  async getCurrentWeather(lat: number = 28.6139, lon: number = 77.2090): Promise<WeatherCurrent> {
    return apiClient<WeatherCurrent>(`/weather/current?latitude=${lat}&longitude=${lon}`);
  },

  async getForecast(lat: number = 28.6139, lon: number = 77.2090): Promise<WeatherForecast> {
    return apiClient<WeatherForecast>(`/weather/forecast?latitude=${lat}&longitude=${lon}`);
  },
};

export const notificationService = {
  async listNotifications(): Promise<NotificationItem[]> {
    return apiClient<NotificationItem[]>('/notifications');
  },

  async markAsRead(notificationId: string): Promise<NotificationItem> {
    return apiClient<NotificationItem>(`/notifications/${notificationId}/read`, {
      method: 'PATCH',
    });
  },

  async markAllAsRead(): Promise<void> {
    return apiClient('/notifications/read-all', { method: 'POST' });
  },
};

export const expertService = {
  async listPendingCases(): Promise<any[]> {
    return apiClient<any[]>('/experts/cases/pending');
  },

  async listCaseHistory(): Promise<any[]> {
    return apiClient<any[]>('/experts/cases/history');
  },

  async submitReview(data: {
    detection_id: string;
    verified_label: string;
    corrected_confidence?: number;
    severity: string;
    is_correct_prediction: boolean;
    notes: string;
    recommendation: string;
  }): Promise<ExpertReview> {
    return apiClient<ExpertReview>('/experts/review', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
};

export const adminService = {
  async getAnalytics(): Promise<AdminAnalytics> {
    return apiClient<AdminAnalytics>('/admin/analytics');
  },

  async listUsers(role?: string): Promise<User[]> {
    const q = role ? `?role=${role}` : '';
    return apiClient<User[]>(`/admin/users${q}`);
  },

  async toggleUserStatus(userId: string, isActive: boolean): Promise<User> {
    return apiClient<User>(`/admin/users/${userId}/status?is_active=${isActive}`, {
      method: 'PATCH',
    });
  },

  async downloadCSV(): Promise<void> {
    const token = localStorage.getItem('agri_access_token');
    const resp = await fetch('http://localhost:8000/api/v1/export/csv', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const blob = await resp.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `crop_scans_export_${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(a);
    a.click();
    a.remove();
  },
};
