import { Routes, Route, Navigate } from 'react-router'
import LoginPage from '../pages/LoginPage/LoginPage.jsx'
import DashboardPage from '../pages/DashboardPage/DashboardPage.jsx'
import VeterinariosPage from '../pages/VeterinariosPage/VeterinariosPage.jsx'
import CitasPage from '../pages/CitasPage/CitasPage.jsx'
import CrearCitaPage from '../pages/CrearCitaPage/CrearCitaPage.jsx'
import PageLayout from '../layout/PageLayout/PageLayout.jsx'


function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route element={<PageLayout />}>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/veterinarios" element={<VeterinariosPage />} />
        <Route path="/citas" element={<CitasPage />} />
        <Route path="/citas/nueva" element={<CrearCitaPage />} />
      </Route>
    </Routes>
  )
}

export default AppRoutes