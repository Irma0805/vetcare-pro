import { createContext, useContext, useState, useMemo } from 'react';
import axiosClient from '../api/axiosClient';
import { getToken, setToken, clearToken } from '../api/tokenStorage';

const AuthContext = createContext(undefined);

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(() => Boolean(getToken()));

  const login = async (username, password) => {
    const response = await axiosClient.post('/login', { username, password });
    setToken(response.data.access_token);
    setIsAuthenticated(true);
  };

  const logout = () => {
    clearToken();
    setIsAuthenticated(false);
  };

  const value = useMemo(
    () => ({ isAuthenticated, login, logout }),
    [isAuthenticated]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth debe usarse dentro de un AuthProvider');
  }
  return context;
}