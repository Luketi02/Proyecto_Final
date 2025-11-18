// src/utils/PrivateRoute.jsx
import { Navigate } from 'react-router-dom';
import { useContext } from 'react';
import AuthContext from '../context/AuthContext';

const PrivateRoute = ({ children }) => {
    let { user } = useContext(AuthContext);

    // Si no hay usuario (no está logueado), lo mandamos al Login
    if (!user) {
        return <Navigate to="/login" />;
    }

    // Si está logueado, dejamos que vea la página (el hijo)
    return children;
};

export default PrivateRoute;