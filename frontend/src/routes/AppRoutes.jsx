import { Routes, Route, Navigate } from 'react-router'
import LoginPage from '../pages/LoginPage/LoginPage.jsx'
import DashboardPage from '../pages/DashboardPage/DashboardPage.jsx'

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
    </Routes>
  )
}

export default AppRoutes