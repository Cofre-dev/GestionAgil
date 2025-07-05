const InventoryApp = {
    // 1. --- PROPIEDADES Y ESTADO ---
    config: {
        apiBaseUrl: '/api',
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
    Modal: {
        elements: { container: null, 
                    title: null,
                    message: null,
                    confirmBtn: null,
                    cancelBtn: null,
                    closeBtn: null
                  },

        confirmCallback: null,

        init() {
            const ids = { container: 'app-modal',
                          title: 'modal-title',
                          message: 'modal-message',
                          confirmBtn: 'modal-confirm-btn',
                          cancelBtn: 'modal-cancel-btn',
                          closeBtn: 'modal-close-btn'
                         };

            for (const key in ids) {
                this.elements[key] = document.getElementById(ids[key]);
            }
            
            this.elements.cancelBtn.addEventListener('click', () => this.hide());

            this.elements.closeBtn.addEventListener('click', () => this.hide());

            this.elements.confirmBtn.addEventListener('click', () => {
                if (this.confirmCallback) this.confirmCallback();
                    this.hide();
            },

            );
        },

        show(title, message, onConfirm) {
            this.elements.title.textContent = title;
            this.elements.message.textContent = message;
            this.confirmCallback = onConfirm;
            this.elements.container.classList.remove('modal-hidden');
        },
        hide() {
            this.elements.container.classList.add('modal-hidden');
            this.confirmCallback = null;
        }
    },

    // 2. --- CICLO DE VIDA DE LA APLICACIÓN ---
    init() {
        if (!this.config.authToken) {
            window.location.href = '/';
            return;
        }
        
        this.elements.authStatus = document.getElementById('auth-status');
        this.elements.itemsContainer = document.getElementById('items-container');
        this.elements.addItemForm = document.getElementById('add-item-form');
        this.elements.movementForm = document.getElementById('movement-form');
        this.elements.itemSelectDropdown = document.getElementById('movement-item');

        this.Modal.init();
        this.setupEventListeners();
        this.renderAuthStatus();
        this.loadInitialData();
    },

    setupEventListeners() {
        this.elements.addItemForm?.addEventListener('submit', (e) => this.handleFormSubmit(e, 'addItem'));
        this.elements.movementForm?.addEventListener('submit', (e) => this.handleFormSubmit(e, 'registerMovement'));
        this.elements.itemsContainer?.addEventListener('click', (event) => {
            const deleteButton = event.target.closest('.delete-button');
            if (deleteButton) {
                this.handleDeleteItem(deleteButton.dataset.id);
            }
        });
    },

    // 3. --- SERVICIO DE API ---
    async apiService(endpoint, method = 'GET', body = null) {
        const headers = new Headers({
            'Content-Type': 'application/json',
            'Authorization': `Token ${this.config.authToken}`
        });
        const config = { method, headers, body: body ? JSON.stringify(body) : null };
        try {
            const response = await fetch(`${this.config.apiBaseUrl}${endpoint}`, config);
            if (!response.ok) {
                const errorData = await response.json();
                const errorMessage = errorData.detail || errorData.error || JSON.stringify(errorData);
                throw new Error(errorMessage);
            }
            return response.status !== 204 ? response.json() : null;
        } catch (error) {
            console.error(`API Error on ${method} ${endpoint}:`, error);
            throw error;
        }
    },

    // 4. --- LÓGICA DE NEGOCIO ---
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
    
    async handleFormSubmit(event, action) {
        event.preventDefault();
        const form = event.target;
        const statusDiv = form.querySelector('.message');
        this.renderMessage(statusDiv, 'Procesando...', 'loading-message');

        try {
            let endpoint, body, successMessage;

            if (action === 'addItem') {
                const formData = new FormData(form);
                body = Object.fromEntries(formData.entries());
                endpoint = '/items/';
                successMessage = `Ítem "${body.nombre}" añadido.`;
            } else if (action === 'registerMovement') {
                body = {
                    item: form.elements['movement-item'].value,
                    tipo_movimiento: 'salida',
                    cantidad_cambio: parseInt(form.elements['movement-quantity'].value),
                    razon: form.elements['movement-reason'].value
                };
                endpoint = '/movements/';
                successMessage = 'Salida registrada exitosamente.';
            }

            await this.apiService(endpoint, 'POST', body);
            this.renderMessage(statusDiv, successMessage, 'stock-ok');
            form.reset();
            this.loadInitialData();
        } catch (error) {
            this.renderMessage(statusDiv, `Error: ${error.message}`, 'error-message');
        }
    },
    
    async handleDeleteItem(itemId) {
        const deleteAction = async () => {
            try {
                await this.apiService(`/items/${itemId}/`, 'DELETE');
                this.loadInitialData();
            } catch (error) {
                this.Modal.show('Error', `No se pudo eliminar el ítem: ${error.message}`, () => {});
            }
        };
        this.Modal.show('Confirmar Eliminación', '¿Estás seguro de que quieres eliminar este ítem permanentemente?', deleteAction);
    },

    // 5. --- RENDERIZADO DEL DOM ---
    renderAuthStatus() {
        if (!this.elements.authStatus) return;
        this.elements.authStatus.innerHTML = `
            <span>Usuario: <strong>${this.config.username || 'N/A'}</strong></span>
            <button id="logout-button" class="logout-button">Cerrar Sesión</button>
        `;
        this.elements.authStatus.querySelector('#logout-button').addEventListener('click', () => {
            localStorage.clear();
            window.location.href = '/';
        });
    },
    
    renderItems(items) {
        const container = this.elements.itemsContainer;
        if (!container) return;
        container.innerHTML = ''; 
        if (items.length === 0) {
            this.renderMessage(container, 'No hay ítems en el inventario.', 'message');
            return;
        }
        const fragment = document.createDocumentFragment(); 
        items.forEach(item => fragment.appendChild(this.createItemCard(item)));
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
            <div class="card-footer">
                <p class="small-text">Registrado: ${new Date(item.fecha_registro).toLocaleDateString()}</p>
                <button class="delete-button" data-id="${item.id}">Eliminar</button>
            </div>
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
        if (element) {
            element.innerHTML = `<p class="${className}">${message}</p>`;
        }
    }
};

// Punto de entrada de la aplicación
document.addEventListener('DOMContentLoaded', () => {
    InventoryApp.init();
});