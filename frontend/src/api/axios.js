// src/api/axios.js
import axios from 'axios';

// Creamos una instancia de Axios con la base URL de tu Django
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/',
    timeout: 5000, // Si tarda más de 5 segundos, cancela
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});

export default api;