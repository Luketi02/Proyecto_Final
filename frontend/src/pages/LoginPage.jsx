// src/pages/LoginPage.jsx
import React, { useContext, useState } from 'react';
import AuthContext from '../context/AuthContext';
import { GoogleLogin } from '@react-oauth/google'; 
import ReCAPTCHA from "react-google-recaptcha";

const LoginPage = () => {
    let { loginUser, loginWithGoogle } = useContext(AuthContext);
    
    const [captchaValido, setCaptchaValido] = useState(false);

    const onChangeCaptcha = (value) => {
        if (value) setCaptchaValido(true);
    };

    const responseGoogle = (response) => {
        console.log("Token de Google:", response.credential);
        loginWithGoogle(response.credential); 
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!captchaValido) {
            alert("Por favor, verifica que no eres un robot 🤖");
            return;
        }
        loginUser(e);
    };

    return (
        <div style={styles.container}>
            <div style={styles.card}>
                <h2>🔐 Iniciar Sesión en IFixNet</h2>
                
                <form onSubmit={handleSubmit} style={styles.form}>
                    <input type="email" name="email" placeholder="Tu Email" style={styles.input} required />
                    <input type="password" name="password" placeholder="Contraseña" style={styles.input} required />
                    
                    <div style={{display: 'flex', justifyContent: 'center', marginBottom: '10px'}}>
                        <ReCAPTCHA
                            sitekey="6LctCRAsAAAAAHmREjIt3h33ZfcDeqTwWRiI9HMc" 
                            onChange={onChangeCaptcha}
                        />
                    </div>

                    <button type="submit" style={styles.button}>Entrar</button>
                </form>

                <div style={styles.divider}>o ingresa con</div>

                <div style={{display: 'flex', justifyContent: 'center', marginTop: '10px'}}>
                    <GoogleLogin
                        onSuccess={responseGoogle}
                        onError={() => {
                            console.log('Login Failed');
                        }}
                        useOneTap
                    />
                </div>

            </div>
        </div>
    )
}

const styles = {
    container: { display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#f0f2f5' },
    card: { padding: '2rem', backgroundColor: 'white', borderRadius: '10px', boxShadow: '0 4px 8px rgba(0,0,0,0.1)', textAlign: 'center', width: '380px' },
    form: { display: 'flex', flexDirection: 'column', gap: '1rem' },
    input: { padding: '10px', borderRadius: '5px', border: '1px solid #ccc' },
    button: { padding: '10px', borderRadius: '5px', border: 'none', backgroundColor: '#007bff', color: 'white', cursor: 'pointer', fontWeight: 'bold' },
    divider: { margin: '1.5rem 0', color: '#888', fontSize: '0.9rem', borderTop: '1px solid #eee', paddingTop: '10px' }
}

export default LoginPage;