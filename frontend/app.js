const BASE_URL = "http://127.0.0.1:8000/api";

// ==================== AUTH ====================
function showLogin() {
    document.getElementById('loginForm').classList.add('active');
    document.getElementById('registerForm').classList.remove('active');
    document.querySelectorAll('.auth-tabs .tab-btn')[0].classList.add('active');
    document.querySelectorAll('.auth-tabs .tab-btn')[1].classList.remove('active');
}

function showRegister() {
    document.getElementById('loginForm').classList.remove('active');
    document.getElementById('registerForm').classList.add('active');
    document.querySelectorAll('.auth-tabs .tab-btn')[0].classList.remove('active');
    document.querySelectorAll('.auth-tabs .tab-btn')[1].classList.add('active');
}

// Register
document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;

    if (!username || !email || !password) {
        showToast('Complete todos los campos', 'error');
        return;
    }

    showLoading(true);
    fetch(`${BASE_URL}/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
    })
    .then(res => res.json())
    .then(data => {
        showLoading(false);
        if (data.message) {
            showToast('Registro exitoso. Ahora inicia sesión.', 'success');
            showLogin();
            document.getElementById('registerForm').reset();
        } else {
            showToast(data.error || 'Error en registro', 'error');
        }
    })
    .catch(() => {
        showLoading(false);
        showToast('Error de conexión', 'error');
    });
});

// Login
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    if (!username || !password) {
        showToast('Usuario y contraseña requeridos', 'error');
        return;
    }

    showLoading(true);
    fetch(`${BASE_URL}/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        showLoading(false);
        if (data.message) {
            localStorage.setItem('loggedIn', 'true');
            localStorage.setItem('username', username);
            showApp();
            showToast('¡Bienvenido!', 'success');
            cargarTareas();
            loadStats();
        } else {
            showToast(data.error || 'Credenciales inválidas', 'error');
        }
    })
    .catch(() => {
        showLoading(false);
        showToast('Error de conexión', 'error');
    });
});

function logout() {
    localStorage.removeItem('loggedIn');
    localStorage.removeItem('username');
    document.getElementById('appSection').classList.add('hidden');
    document.getElementById('authSection').classList.remove('hidden');
    document.querySelectorAll('form')[0].reset();
    document.querySelectorAll('form')[1].reset();
    showToast('Sesión cerrada', 'info');
}

// ==================== TASK FORM ====================
function toggleTaskForm() {
    const form = document.getElementById('taskForm');
    form.classList.toggle('hidden');
    if (!form.classList.contains('hidden')) {
        document.getElementById('taskTitle').focus();
    }
}

function cancelEdit() {
    document.getElementById('taskForm').classList.add('hidden');
    document.getElementById('taskForm').reset();
    document.getElementById('editTaskId').value = '';
    document.getElementById('saveTaskBtn').textContent = 'Crear Tarea';
    document.querySelector('.cancel-btn').classList.add('hidden');
}

document.getElementById('taskForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const id = document.getElementById('editTaskId').value;
    const title = document.getElementById('taskTitle').value;
    const description = document.getElementById('taskDescription').value;
    const status = document.getElementById('taskStatus').value;

    if (!title.trim()) {
        showToast('El título es obligatorio', 'error');
        return;
    }

    const data = { titulo: title, descripcion: description, estado: status };
    const method = id ? 'PUT' : 'POST';
    const url = id ? `${BASE_URL}/tasks/${id}/update/` : `${BASE_URL}/tasks/create/`;

    showLoading(true);
    fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(() => {
        showLoading(false);
        showToast(id ? 'Tarea actualizada' : 'Tarea creada', 'success');
        cancelEdit();
        cargarTareas();
        loadStats();
    })
    .catch(() => {
        showLoading(false);
        showToast('Error al guardar', 'error');
    });
});

// ==================== TASKS LIST ====================
function cargarTareas() {
    showLoading(true);
    fetch(`${BASE_URL}/tasks/`)
    .then(res => res.json())
    .then(tasks => {
        showLoading(false);
        const list = document.getElementById('taskList');
        const noTasks = document.getElementById('noTasks');
        
        if (tasks.length === 0) {
            list.innerHTML = '';
            noTasks.classList.remove('hidden');
            return;
        }
        
        noTasks.classList.add('hidden');
        list.innerHTML = tasks.map(task => createTaskElement(task)).join('');
    })
    .catch(() => {
        showLoading(false);
        showToast('Error cargando tareas', 'error');
    });
}

function createTaskElement(task) {
    const statusClass = task.estado?.toLowerCase() === 'completada' ? 'completed' : 
                       task.estado?.toLowerCase() === 'en progreso' ? 'progress' : 'pending';
    const statusIcon = task.estado?.toLowerCase() === 'completada' ? 'fa-check-circle' : 
                      task.estado?.toLowerCase() === 'en progreso' ? 'fa-spinner' : 'fa-clock';
    
    return `
        <li class="task-card ${statusClass}">
            <div class="task-header">
                <h3>${task.titulo || task.title}</h3>
                <span class="status-badge">
                    <i class="fas ${statusIcon}"></i>
                    ${task.estado || task.status || 'Pendiente'}
                </span>
            </div>
            ${task.descripcion || task.description ? `<p class="task-desc">${task.descripcion || task.description}</p>` : ''}
            <div class="task-actions">
                <button onclick="editTask('${task.id}')" class="btn-edit" title="Editar">
                    <i class="fas fa-edit"></i>
                </button>
                <button onclick="updateStatus('${task.id}', '${task.estado === 'Completada' ? 'Pendiente' : 'Completada'}')" class="btn-toggle" title="Toggle completada">
                    <i class="fas fa-exchange-alt"></i>
                </button>
                <button onclick="deleteTask('${task.id}')" class="btn-delete" title="Eliminar">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </li>
    `;
}

function editTask(id) {
    fetch(`${BASE_URL}/tasks/`)
    .then(res => res.json())
    .then(tasks => {
        const task = tasks.find(t => t.id === id);
        if (task) {
            document.getElementById('editTaskId').value = id;
            document.getElementById('taskTitle').value = task.titulo || task.title || '';
            document.getElementById('taskDescription').value = task.descripcion || task.description || '';
            document.getElementById('taskStatus').value = task.estado || task.status || 'Pendiente';
            document.getElementById('saveTaskBtn').textContent = 'Actualizar Tarea';
            document.querySelector('.cancel-btn').classList.remove('hidden');
            toggleTaskForm();
        }
    });
}

function updateStatus(id, newStatus) {
    fetch(`${BASE_URL}/tasks/${id}/update/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ estado: newStatus })
    })
    .then(res => res.json())
    .then(() => {
        showToast('Estado actualizado', 'success');
        cargarTareas();
        loadStats();
    })
    .catch(() => showToast('Error actualizando', 'error'));
}

function deleteTask(id) {
    if (confirm('¿Eliminar esta tarea?')) {
        fetch(`${BASE_URL}/tasks/${id}/delete/`, { method: 'DELETE' })
        .then(res => res.json())
        .then(() => {
            showToast('Tarea eliminada', 'success');
            cargarTareas();
            loadStats();
        })
        .catch(() => showToast('Error eliminando', 'error'));
    }
}

// ==================== STATS ====================
function loadStats() {
    fetch(`${BASE_URL}/tasks/counter/`)
    .then(res => res.json())
    .then(stats => {
        document.getElementById('totalTasks').textContent = stats.cantidad;
        document.getElementById('pendingTasks').textContent = stats.pendientes;
        document.getElementById('progressTasks').textContent = stats.en_progreso;
        document.getElementById('completedTasks').textContent = stats.completada;
    })
    .catch(() => {
        // Fallback to 0 if error
        document.querySelectorAll('[id*="Tasks"]').forEach(el => el.textContent = "0");
    });
}

// ==================== UTILS ====================
function showApp() {
    document.getElementById('authSection').classList.add('hidden');
    document.getElementById('appSection').classList.remove('hidden');
    document.getElementById('usernameDisplay').textContent = localStorage.getItem('username') || 'Usuario';
    document.getElementById('userStatus').classList.remove('hidden');
}

function showLoading(show = true) {
    document.getElementById('loading').classList.toggle('hidden', !show);
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), 3000);
}

// ==================== INIT ====================
document.addEventListener('DOMContentLoaded', function() {
    if (localStorage.getItem('loggedIn') === 'true') {
        showApp();
        cargarTareas();
        loadStats();
    }
});

