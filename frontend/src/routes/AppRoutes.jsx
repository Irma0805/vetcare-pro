import { Routes, Route } from 'react-router'

function Placeholder() {
  return <p>VetCare Pro — routing funcionando correctamente</p>
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Placeholder />} />
    </Routes>
  )
}

export default AppRoutes