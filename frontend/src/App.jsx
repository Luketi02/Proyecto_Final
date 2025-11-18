// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import LoginPage from './pages/LoginPage';
import PrivateRoute from './utils/PrivateRoute'; // <-- 1. Importamos el Patovica

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          
          {/* 2. Protegemos la ruta Home */}
          <Route 
            path="/" 
            element={
              <PrivateRoute>
                 {/* Todo lo que pongas acá adentro es privado */}
                 <div style={{textAlign: 'center', marginTop: '50px'}}>
                    <h1>🏠 Bienvenido al Sistema IFixNet</h1>
                    <p>Si ves esto, ¡estás logueado y autorizado!</p>
                 </div>
              </PrivateRoute>
            } 
          />
          
        </Routes>
      </AuthProvider>
    </Router>
  )
}

export default App;