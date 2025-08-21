import { authAPI } from './api';

class AuthService {
  constructor() {
    this.token = localStorage.getItem('access_token');
    this.user = JSON.parse(localStorage.getItem('user') || 'null');
  }

  async login(email, password) {
    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);
      
      const response = await authAPI.login(formData);
      
      if (response.data.access_token) {
        this.token = response.data.access_token;
        this.user = { email }; // Basit kullanıcı bilgisi
        
        localStorage.setItem('access_token', this.token);
        localStorage.setItem('user', JSON.stringify(this.user));
        
        return { success: true, user: this.user };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Giriş başarısız' 
      };
    }
  }

  logout() {
    this.token = null;
    this.user = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  }

  isAuthenticated() {
    return !!this.token;
  }

  getToken() {
    return this.token;
  }

  getUser() {
    return this.user;
  }

  // Token süresi kontrolü (basit)
  isTokenExpired() {
    if (!this.token) return true;
    
    try {
      const payload = JSON.parse(atob(this.token.split('.')[1]));
      return payload.exp * 1000 < Date.now();
    } catch {
      return true;
    }
  }
}

export const authService = new AuthService();
