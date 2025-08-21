import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/auth';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(authService.getUser());
  const [isAuthenticated, setIsAuthenticated] = useState(authService.isAuthenticated());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Sayfa yüklendiğinde auth durumunu kontrol et
    checkAuth();
  }, []);

  const checkAuth = () => {
    const authenticated = authService.isAuthenticated() && !authService.isTokenExpired();
    setIsAuthenticated(authenticated);
    
    if (authenticated) {
      setUser(authService.getUser());
    } else {
      authService.logout();
      setUser(null);
    }
    
    setLoading(false);
  };

  const login = async (email, password) => {
    setLoading(true);
    const result = await authService.login(email, password);
    
    if (result.success) {
      setUser(result.user);
      setIsAuthenticated(true);
    }
    
    setLoading(false);
    return result;
  };

  const logout = () => {
    authService.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    logout,
    checkAuth
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
