// gestionAgil/static/js/script.js
const API_BASE_URL = 'http://127.0.0.1:8000/api';
const TOKEN_AUTH_URL = 'http://127.0.0.1:8000/api-token-auth/';

const itemsContainer = document.getElementById('items-container');
const loginForm = document.getElementById('login-form');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const authStatusDiv = document.getElementById('auth-status');
const addItemForm = document.getElementById('add-item-form');
const addItemStatusDiv = document.getElementById('add-item-status');

let authToken = localStorage.getItem('authToken'); // Cargar token guardado
let isAuthenticated = !!authToken; // Convertir a booleano

// --- Funciones de Autenticación ---

function updateAuthStatus() {
    if (isAuthenticated) {
        authStatusDiv.innerHTML = `<strong>Autenticado como: ${localStorage.getItem('username')}</strong> <button class="logout-button" onclick="logout()">Cerrar Sesión</button>`;
        loginForm.style.display = 'none'; // Ocultar formulario de login
        addItemForm.style.display = 'block'; // Mostrar formulario de añadir ítem
    } else {
        authStatusDiv.innerHTML = `No autenticado.`;
        loginForm.style.display = 'block'; // Mostrar formulario de login
        addItemForm.style.display = 'none'; // Ocultar formulario de añadir ítem
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
            throw new Error(errorData.non_field_errors ? errorData.non_field_errors[0] : 'Error al iniciar sesión.');
        }

        const data = await response.json();
        authToken = data.token;
        localStorage.setItem('authToken', authToken); // Guardar token
        localStorage.setItem('username', username); // Guardar username
        isAuthenticated = true;
        updateAuthStatus();
        fetchItems(); // Recargar ítems con posible autorización
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
    fetchItems(); // Recargar ítems (mostrará solo lectura si es el caso)
}

// --- Funciones para Ítems de Inventario ---

async function fetchItems() {
    itemsContainer.innerHTML = '<p class="message loading-message">Cargando ítems...</p>';
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
        itemsContainer.innerHTML = `<p class="message error-message">${error.message || 'Error al cargar ítems. Verifique la consola para más detalles.'}</p>`;
    }
}

function renderItems(items) {
    if (items.length === 0) {
        itemsContainer.innerHTML = '<p class="message">No hay ítems en el inventario.</p>';
        return;
    }

    itemsContainer.innerHTML = ''; // Limpiar contenido existente
    items.forEach(item => {
        const itemCard = document.createElement('div');
        itemCard.className = 'item-card';
        const stockStatusClass = item.cantidad < item.umbral_minimo ? 'stock-bajo' : 'stock-ok';

        itemCard.innerHTML = `
            <h3>${item.nombre}</h3>
            <p><strong>Descripción:</strong> ${item.descripcion || 'N/A'}</p>
            <p><strong>Número de Serie:</strong> ${item.numero_serie || 'N/A'}</p>
            <p><strong>Ubicación:</strong> <span class="math-inline">\{item\.ubicacion \|\| 'N/A'\}</p\>
<p><strong>Cantidad:</strong> <span class="{stockStatusClass}">${item.cantidad}</span></p>
<p><strong>Umbral Mínimo:</strong> ${item.umbral_minimo}</p>
<p class="small-text">Registrado: ${new Date(item.fecha_registro).toLocaleDateString()}</p>
`;
itemsContainer.appendChild(itemCard);
});
}

async function addItem(event) {
    event.preventDefault();
    addItemStatusDiv.innerHTML = ''; // Limpiar mensaje anterior

    if (!isAuthenticated) {
        addItemStatusDiv.className = 'message error-message';
        addItemStatusDiv.textContent = 'Debes iniciar sesión para añadir ítems.';
        return;
    }

    const newItem = {
        nombre: document.getElementById('item-nombre').value,
        descripcion: document.getElementById('item-descripcion').value,
        numero_serie: document.getElementById('item-numero_serie').value,
        cantidad: parseInt(document.getElementById('item-cantidad').value),
        ubicacion: document.getElementById('item-ubicacion').value,
        umbral_minimo: parseInt(document.getElementById('item-umbral_minimo').value),
        // Las categorías y etiquetas no se manejan en este formulario simple, serían IDs.
        // Asignamos valores predeterminados o los omitimos por simplicidad en este ejemplo.
        categorias: [], // Django REST Framework espera un array de IDs para ManyToMany
        etiquetas: [],   // Django REST Framework espera un array de IDs para ManyToMany
    };

    // Validaciones básicas del lado del cliente
    if (!newItem.nombre || isNaN(newItem.cantidad) || isNaN(newItem.umbral_minimo)) {
        addItemStatusDiv.className = 'message error-message';
        addItemStatusDiv.textContent = 'Por favor, rellena los campos obligatorios (Nombre, Cantidad, Umbral Mínimo) con valores válidos.';
        return;
    }
    if (newItem.cantidad < 0 || newItem.umbral_minimo < 0) {
        addItemStatusDiv.className = 'message error-message';
        addItemStatusDiv.textContent = 'La cantidad y el umbral mínimo no pueden ser negativos.';
        return;
    }


    try {
        const response = await fetch(`${API_BASE_URL}/items/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${authToken}`, // Enviar token en el header
            },
            body: JSON.stringify(newItem),
        });

        if (!response.ok) {
            const errorData = await response.json(); // Intentar leer el cuerpo del error
            let errorMessage = 'Error al añadir ítem.';
            if (errorData) {
                errorMessage += ` Detalles: ${JSON.stringify(errorData)}`;
            }
            throw new Error(errorMessage);
        }

        const addedItem = await response.json();
        addItemStatusDiv.className = 'message stock-ok';
        addItemStatusDiv.textContent = `Ítem "${addedItem.nombre}" añadido exitosamente!`;
        addItemForm.reset(); // Limpiar formulario
        fetchItems(); // Recargar la lista de ítems
    } catch (error) {
        console.error('Error adding item:', error);
        addItemStatusDiv.className = 'message error-message';
        addItemStatusDiv.textContent = `Error al añadir ítem: ${error.message}`;
    }
}


// --- Event Listeners y Carga Inicial ---
loginForm.addEventListener('submit', login);
addItemForm.addEventListener('submit', addItem);

// Ejecutar al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    updateAuthStatus(); // Actualizar estado de autenticación al cargar
    fetchItems(); // Cargar ítems
});
``