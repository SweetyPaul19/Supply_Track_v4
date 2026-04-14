import { createContext, useState, useEffect, useContext, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

const API = 'http://127.0.0.1:5000/api';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token      = localStorage.getItem('token');
    const storedUser = localStorage.getItem('shopUser');
    if (token && storedUser) {
      setUser(JSON.parse(storedUser));
      // Always re-fetch fresh profile so green_credits are current
      axios.get(`${API}/auth/profile`, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(r => {
        localStorage.setItem('shopUser', JSON.stringify(r.data));
        setUser(r.data);
      }).catch(() => {});
    }
  }, []);

  const login = (token, userData) => {
    localStorage.setItem('token', token);
    localStorage.setItem('shopUser', JSON.stringify(userData));
    setUser(userData);
    navigate('/');
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('shopUser');
    setUser(null);
    navigate('/auth');
  };

  // Call after placing an order to refresh green_credits live in nav
  const refreshProfile = useCallback(async () => {
    const token = localStorage.getItem('token');
    if (!token) return;
    try {
      const r = await axios.get(`${API}/auth/profile`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      localStorage.setItem('shopUser', JSON.stringify(r.data));
      setUser(r.data);
    } catch (e) {
      console.error('Could not refresh profile', e);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, refreshProfile }}>
      {children}
    </AuthContext.Provider>
  );
};
