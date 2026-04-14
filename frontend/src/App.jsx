import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import AdminDashboard from './pages/AdminDashboard';
import ShopDashboard from './pages/ShopDashboard';
import AuthPage from './pages/AuthPage';
import TruckView from './components/TruckView';

const ProtectedRoute = ({ children }) => {
  const { user } = useAuth();
  if (!user) return <Navigate to="/auth" />;
  return children;
};

function App() {
  return (
    <Routes>
      <Route path="/auth" element={<AuthPage />} />

      {/* Shop owner marketplace dashboard */}
      <Route path="/" element={
        <ProtectedRoute><ShopDashboard /></ProtectedRoute>
      } />

      {/* Admin / fleet view */}
      <Route path="/fleet" element={
        <ProtectedRoute><AdminDashboard /></ProtectedRoute>
      } />

      {/* Individual truck IoT view */}
      <Route path="/truck/:id" element={
        <ProtectedRoute><TruckView /></ProtectedRoute>
      } />
    </Routes>
  );
}

export default App;
