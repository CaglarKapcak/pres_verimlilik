import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const machineAPI = {
  getAll: () => api.get('/api/machines/'),
  getById: (id) => api.get(`/api/machines/${id}`),
  getOEE: (id, startTime, endTime) => 
    api.get(`/api/machines/${id}/oee?start_time=${startTime}&end_time=${endTime}`),
  sendData: (id, data) => api.post(`/api/machines/${id}/data`, data),
};

export const authAPI = {
  login: (credentials) => api.post('/api/auth/token', credentials),
};

export default api;
