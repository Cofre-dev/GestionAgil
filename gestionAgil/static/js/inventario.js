/**
 * InventoryApp
 * Objeto que encapsula toda la funcionalidad de la página de administración de inventario.
 */
const InventoryApp = {
    
    // 1. --- ESTADO Y CONFIGURACIÓN ---
    // Centralizamos la configuración y las referencias a elementos del DOM.
    config: {
        apiBaseUrl: '/api', // Usamos rutas relativas, más flexibles
        authToken: localStorage.getItem('authToken'),
        username: localStorage.getItem('username')
    },

    elements: {
        authStatus: null,
        itemsContainer: null,
        addItemForm: null,
        movementForm: null,
        itemSelectDropdown: null
    },

    // 2. --- MÉTODO DE INICIALIZACIÓN ---
    // El punto de entrada que arranca la aplicación.
    init() {
        // Verificamos la autenticación primero
        if (!this.config.authToken) {
            window.location.href = '/';
            return;
        }

        // Asignamos los elementos del DOM una sola vez
        this.elements.authStatus = document.getElementById('auth-status');
        this.elements.itemsContainer = document.getElementById('items-container');
        this.elements.addItemForm = document.getElementById('add-item-form');
        this.elements.movementForm = document.getElementById('movement-form');
        this.elements.itemSelectDropdown = document.getElementById('movement-item');

        this.setupEventListeners();
        this.renderAuthStatus();
        this.loadInitialData();
    },

    // 3. --- MANEJO DE EVENTOS ---
    // Centralizamos la configuración de todos los event listeners.
    setupEventListeners() {
        this.elements.addItemForm?.addEventListener('submit', (e) => this.handleAddItem(e));
        this.elements.movementForm?.addEventListener('submit', (e) => this.handleRegisterMovement(e));
    },

    // 4. --- LÓGICA DE LA API ---
    // Una única función para manejar todas las llamadas a la API, evitando repetición.
    async apiService(endpoint, method = 'GET', body = null) {
        const headers = new Headers({
            'Content-Type': 'application/json',
            'Authorization': `Token ${this.config.authToken}`
        });

        const config = {
            method,
            headers,
            body: body ? JSON.stringify(body) : null
        };

        try {
            const response = await fetch(`${this.config.apiBaseUrl}${endpoint}`, config);
            if (!response.ok) {
                const errorData = await response.json();
                // Extraemos el mensaje de error más específico si existe
                const errorMessage = errorData.detail || errorData.error || JSON.stringify(errorData);
                throw new Error(errorMessage);
            }
            // Si la respuesta no tiene contenido (ej: DELETE), no intentamos parsear JSON
            return response.status !== 204 ? response.json() : null;
        } catch (error) {
            console.error(`API Error on ${method} ${endpoint}:`, error);
            throw error; // Re-lanzamos el error para que sea manejado por la función que llama
        }
    },

    // 5. --- LÓGICA DE NEGOCIO ---
    // Funciones que orquestan las llamadas a la API y la renderización.
    async loadInitialData() {
        this.renderMessage(this.elements.itemsContainer, 'Cargando ítems...', 'loading-message');
        try {
            const items = await this.apiService('/items/');
            this.renderItems(items);
            this.populateItemsDropdown(items);
        } catch (error) {
            this.renderMessage(this.elements.itemsContainer, `Error al cargar ítems: ${error.message}`, 'error-message');
        }
    },

  async handleAddItem(event) {
    event.preventDefault();
    const form = event.target;
    const statusDiv = form.querySelector('.message'); // Usamos un selector más específico

    try {
        // Convierte automáticamente el formulario a un objeto JS
        const formData = new FormData(form);
        const newItem = Object.fromEntries(formData.entries());

        // Aseguramos que los números sean números y no strings
        newItem.cantidad = parseInt(newItem.cantidad);
        newItem.umbral_minimo = parseInt(newItem.umbral_minimo);

        this.renderMessage(statusDiv, 'Añadiendo...', 'loading-message');
        
        const addedItem = await this.apiService('/items/', 'POST', newItem);
        
        this.renderMessage(statusDiv, `Ítem "${addedItem.nombre}" añadido exitosamente.`, 'stock-ok');
        form.reset();
        this.loadInitialData(); // Recargamos todo para mantener la consistencia

    } catch (error) {
        this.renderMessage(statusDiv, `Error: ${error.message}`, 'error-message');
    }
},

    async handleRegisterMovement(event) {
        event.preventDefault();
        const form = event.target;
        const statusDiv = form.querySelector('.message');
        
        const movementData = {
            item: form.elements['movement-item'].value,
            tipo_movimiento: 'salida',
            cantidad_cambio: parseInt(form.elements['movement-quantity'].value),
            razon: form.elements['movement-reason'].value
        };

        try {
            this.renderMessage(statusDiv, 'Procesando salida...', 'loading-message');
            await this.apiService('/movements/', 'POST', movementData);
            this.renderMessage(statusDiv, 'Salida registrada exitosamente.', 'stock-ok');
            form.reset();
            this.loadInitialData();
        } catch (error) {
            this.renderMessage(statusDiv, `Error: ${error.message}`, 'error-message');
        }
    },

    // 6. --- RENDERIZADO Y MANIPULACIÓN DEL DOM ---
    // Funciones dedicadas exclusivamente a actualizar la interfaz.
    renderAuthStatus() {
        const statusDiv = this.elements.authStatus;
        if (!statusDiv) return;

        statusDiv.innerHTML = `
            <span>Usuario: <strong>${this.config.username || 'N/A'}</strong></span>
            <button id="logout-button">Cerrar Sesión</button>
        `;
        statusDiv.querySelector('#logout-button').addEventListener('click', () => {
            localStorage.clear();
            window.location.href = '/';
        });
    },
    
    renderItems(items) {
        const container = this.elements.itemsContainer;
        if (!container) return;

        if (items.length === 0) {
            this.renderMessage(container, 'No hay ítems en el inventario.', 'message');
            return;
        }

        container.innerHTML = ''; 
        const fragment = document.createDocumentFragment(); 
        items.forEach(item => {
            const itemCard = this.createItemCard(item);
            fragment.appendChild(itemCard);
        });
        container.appendChild(fragment);
    },

    createItemCard(item) {
        const card = document.createElement('div');
        card.className = 'item-card';
        const stockStatusClass = item.cantidad < item.umbral_minimo ? 'stock-bajo' : 'stock-ok';
        
        card.innerHTML = `
            <h3>${item.nombre}</h3>
            <p><strong>N/S:</strong> ${item.numero_serie || 'N/A'}</p>
            <p><strong>Ubicación:</strong> ${item.ubicacion || 'N/A'}</p>
            <p><strong>Cantidad:</strong> <span class="${stockStatusClass}">${item.cantidad}</span> (Mín: ${item.umbral_minimo})</p>
            <p class="small-text">Registrado: ${new Date(item.fecha_registro).toLocaleDateString()}</p>
        `;
        return card;
    },

    populateItemsDropdown(items) {
        const dropdown = this.elements.itemSelectDropdown;
        if (!dropdown) return;

        dropdown.innerHTML = '<option value="" disabled selected>-- Elige un ítem --</option>';
        items.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            option.textContent = `${item.nombre} (Stock: ${item.cantidad})`;
            dropdown.appendChild(option);
        });
    },

    renderMessage(element, message, className) {
        if (!element) return;
        element.innerHTML = `<p class="${className}">${message}</p>`;
    }
};

// Punto de entrada: cuando el DOM está listo, inicializamos la aplicación.
document.addEventListener('DOMContentLoaded', () => {
    InventoryApp.init();
});