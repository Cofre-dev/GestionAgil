document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const authStatusDiv = document.getElementById('auth-status');
    const API_TOKEN_URL = 'http://127.0.0.1:8000/api-token-auth/'; // URL directa al token

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        authStatusDiv.textContent = 'Procesando...';
        authStatusDiv.className = 'auth-status';

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(API_TOKEN_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                throw new Error('Usuario o contraseña incorrectos.');
            }

            const data = await response.json();
            
            // 1. Guardar el token
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('username', username);

            // 2. Redirigir a la página de inventario
            window.location.href = '/inventario/';

        } catch (error) {
            authStatusDiv.textContent = error.message;
            authStatusDiv.classList.add('error-message');
        }
    });
});