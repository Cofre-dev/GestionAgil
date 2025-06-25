// gestionAgil/static/js/script.js

// Envuelve todo tu código en esta función para asegurar que el DOM esté cargado
document.addEventListener('DOMContentLoaded', () => {

    const API_BASE_URL = 'http://127.0.0.1:8000/api';
    const TOKEN_AUTH_URL = 'http://127.0.0.1:8000/api-token-auth/';

    // Asegúrate de que todos estos IDs existan en tu HTML
    const itemsContainer = document.getElementById('items-container');
    const loginForm = document.getElementById('login-form');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const authStatusDiv = document.getElementById('auth-status');
    const addItemForm = document.getElementById('add-item-form');
    const addItemStatusDiv = document.getElementById('add-item-status');

    let authToken = localStorage.getItem('authToken');
    let isAuthenticated = !!authToken;

    // --- Funciones de Autenticación ---

    function updateAuthStatus() {
        // VERIFICACIONES ADICIONALES PARA DEBUGGING:
        // console.log("updateAuthStatus called.");
        // console.log("loginForm:", loginForm);
        // console.log("addItemForm:", addItemForm);

        if (isAuthenticated) {
            if (authStatusDiv) authStatusDiv.innerHTML = `<strong>Autenticado como: ${localStorage.getItem('username')}</strong> <button class="logout-button" onclick="logout()">Cerrar Sesión</button>`;
            if (loginForm) loginForm.style.display = 'none'; // Aquí es donde ocurría el error si loginForm era null
            if (addItemForm) addItemForm.style.display = 'block'; // Y aquí si addItemForm era null
        } else {
            if (authStatusDiv) authStatusDiv.innerHTML = `No autenticado.`;
            if (loginForm) loginForm.style.display = 'block';
            if (addItemForm) addItemForm.style.display = 'none';
        }
    }

    async function login(event) {
        event.preventDefault();
        const username = usernameInput.value;
        const password = passwordInput.value;

        try {
            const response = await fetch(TOKEN_AUTH_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.non_field_errors ? errorData.non_field_errors[0] : 'Credenciales inválidas.'); // Mensaje más específico
            }

            const data = await response.json();
            authToken = data.token;
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('username', username);
            isAuthenticated = true;
            updateAuthStatus();
            fetchItems();
            alert('¡Inicio de sesión exitoso!');
        } catch (error) {
            console.error('Login error:', error);
            alert(`Error de inicio de sesión: ${error.message}`);
        }
    }

    function logout() {
        authToken = null;
        isAuthenticated = false;
        localStorage.removeItem('authToken');
        localStorage.removeItem('username');
        updateAuthStatus();
        alert('Sesión cerrada.');
        fetchItems();
    }

    // --- Funciones para Ítems de Inventario ---

    async function fetchItems() {
        if (itemsContainer) itemsContainer.innerHTML = '<p class="message loading-message">Cargando ítems...</p>'; // Asegurarse de que itemsContainer no sea null
        try {
            const headers = {};
            if (isAuthenticated) {
                headers['Authorization'] = `Token ${authToken}`;
            }
            const response = await fetch(`${API_BASE_URL}/items/`, { headers });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Error ${response.status}: ${errorText}`);
            }

            const items = await response.json();
            renderItems(items);
        } catch (error) {
            console.error('Error fetching items:', error);
            if (itemsContainer) itemsContainer.innerHTML = `<p class="message error-message">${error.message || 'Error al cargar ítems. Verifique la consola para más detalles.'}</p>`;
        }
    }

    function renderItems(items) {
        if (!itemsContainer) return; // Salir si el contenedor no existe

        if (items.length === 0) {
            itemsContainer.innerHTML = '<p class="message">No hay ítems en el inventario.</p>';
            return;
        }

        itemsContainer.innerHTML = '';
        items.forEach(item => {
            const itemCard = document.createElement('div');
            itemCard.className = 'item-card';
            const stockStatusClass = item.cantidad < item.umbral_minimo ? 'stock-bajo' : 'stock-ok';

            itemCard.innerHTML = `
                <h3>${item.nombre}</h3>
                <p><strong>Descripción:</strong> ${item.descripcion || 'N/A'}</p>
                <p><strong>Número de Serie:</strong> ${item.numero_serie || 'N/A'}</p>
                <p><strong>Ubicación:</strong> ${item.ubicacion || 'N/A'}</p>
                <p><strong>Cantidad:</strong> <span class="${stockStatusClass}">${item.cantidad}</span></p>
                <p><strong>Umbral Mínimo:</strong> ${item.umbral_minimo}</p>
                <p class="small-text">Registrado: ${new Date(item.fecha_registro).toLocaleDateString()}</p>
            `;
            itemsContainer.appendChild(itemCard);
        });
    }

    async function addItem(event) {
        event.preventDefault();
        if (addItemStatusDiv) addItemStatusDiv.innerHTML = '';

        if (!isAuthenticated) {
            if (addItemStatusDiv) {
                addItemStatusDiv.className = 'message error-message';
                addItemStatusDiv.textContent = 'Debes iniciar sesión para añadir ítems.';
            }
            return;
        }

        const newItem = {
            nombre: document.getElementById('item-nombre').value,
            descripcion: document.getElementById('item-descripcion').value,
            numero_serie: document.getElementById('item-numero_serie').value,
            cantidad: parseInt(document.getElementById('item-cantidad').value),
            ubicacion: document.getElementById('item-ubicacion').value,
            umbral_minimo: parseInt(document.getElementById('item-umbral_minimo').value),
            categorias: [],
            etiquetas: [],
        };

        if (!newItem.nombre || isNaN(newItem.cantidad) || isNaN(newItem.umbral_minimo)) {
            if (addItemStatusDiv) {
                addItemStatusDiv.className = 'message error-message';
                addItemStatusDiv.textContent = 'Por favor, rellena los campos obligatorios (Nombre, Cantidad, Umbral Mínimo) con valores válidos.';
            }
            return;
        }
         if (newItem.cantidad < 0 || newItem.umbral_minimo < 0) {
            if (addItemStatusDiv) {
                addItemStatusDiv.className = 'message error-message';
                addItemStatusDiv.textContent = 'La cantidad y el umbral mínimo no pueden ser negativos.';
            }
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/items/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${authToken}`,
                },
                body: JSON.stringify(newItem),
            });

            if (!response.ok) {
                const errorData = await response.json();
                let errorMessage = 'Error al añadir ítem.';
                if (errorData) {
                    errorMessage += ` Detalles: ${JSON.stringify(errorData)}`;
                }
                throw new Error(errorMessage);
            }

            const addedItem = await response.json();
            if (addItemStatusDiv) {
                addItemStatusDiv.className = 'message stock-ok';
                addItemStatusDiv.textContent = `Ítem "${addedItem.nombre}" añadido exitosamente!`;
            }
            if (addItemForm) addItemForm.reset();
            fetchItems();
        } catch (error) {
            console.error('Error adding item:', error);
            if (addItemStatusDiv) {
                addItemStatusDiv.className = 'message error-message';
                addItemStatusDiv.textContent = `Error al añadir ítem: ${error.message}`;
            }
        }
    }


    // --- Event Listeners y Carga Inicial ---
    // Asegurarse de que los elementos existan antes de añadir listeners
    if (loginForm) loginForm.addEventListener('submit', login);
    if (addItemForm) addItemForm.addEventListener('submit', addItem);

    updateAuthStatus();
    fetchItems();

}); // Fin de DOMContentLoaded