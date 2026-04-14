import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 🔑 Attach token to every request
instance.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem('token'); // ✅ correct storage
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default instance;