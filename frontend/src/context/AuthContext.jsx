// src/context/AuthContext.jsx
import { createContext, useState } from 'react';
import { jwtDecode } from "jwt-decode";
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
    
    let [authTokens, setAuthTokens] = useState(() => 
        localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null
    );
    
    let [user, setUser] = useState(() => 
        localStorage.getItem('authTokens') ? jwtDecode(localStorage.getItem('authTokens')) : null
    );

    const navigate = useNavigate();

    // --- LOGIN NORMAL (Email y Contraseña) ---
    let loginUser = async (e) => {
        e.preventDefault();
        let response = await api.post('token/', {
            email: e.target.email.value,
            password: e.target.password.value
        }).catch(() => {
            alert("Error: Email o contraseña incorrectos 😢");
        });

        if (response && response.status === 200) {
            setAuthTokens(response.data);
            setUser(jwtDecode(response.data.access));
            localStorage.setItem('authTokens', JSON.stringify(response.data));
            navigate('/'); 
        }
    }

    // --- LOGIN CON GOOGLE ---
    let loginWithGoogle = async (googleToken) => {
        // Llamamos a la vista especial que creamos en Django
        let response = await api.post('auth/google/', {
            token: googleToken
        }).catch(error => {
            alert("Algo falló al conectar con Google 😢");
            console.log(error);
        });

        if (response && response.status === 200) {
            // Si Django nos da el OK, guardamos todo igual que en el login normal
            setAuthTokens(response.data);
            setUser(jwtDecode(response.data.access));
            localStorage.setItem('authTokens', JSON.stringify(response.data));
            navigate('/'); 
        }
    }

    // --- LOGOUT ---
    let logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
        navigate('/login');
    }

    // Empaquetamos todo
    let contextData = {
        user: user,
        authTokens: authTokens,
        loginUser: loginUser,
        loginWithGoogle: loginWithGoogle, 
        logoutUser: logoutUser,
    }

    return (
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    )
}