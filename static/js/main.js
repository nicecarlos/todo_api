const API_URL = '/api/tasks';

let tasks = [];

document.addEventListener('DOMContentLoaded', () => {
    loadTasks();

    const taskForm = document.getElementById('task-form');
    taskForm.addEventListener('submit', createTask);
});



// 1. LISTAR TAREFAS (GET)
async function loadTasks() {
    try {
        const response = await fetch(API_URL);
        tasks = await response.json();
        renderTasks(tasks);
    } catch (error) {
        console.error('Erro ao carregar tarefas:', error);
    }
}

// 2. RENDERIZAR NA TELA
function renderTasks(tasks) {
    const taskList = document.getElementById('task-list');
    taskList.innerHTML = '';

    if (tasks.length === 0) {
        taskList.innerHTML = '<li style="text-align:center; color:#7f8c8d;">Nenhuma tarefa encontrada.</li>';
        return;
    }

    tasks.forEach(task => {
        const li = document.createElement('li');
        li.className = `task-item ${task.completed ? 'completed' : ''}`;

        li.innerHTML = `
            <div class="task-info">
                <h3>${escapeHtml(task.title)}</h3>
                ${task.description ? `<p>${escapeHtml(task.description)}</p>` : ''}
            </div>
            <div class="task-actions">
                <button class="btn btn-done" onclick="toggleTask(${task.id}, ${!task.completed})">
                    ${task.completed ? 'Desfazer' : 'Concluir'}
                </button>
                <button class="btn btn-delete" onclick="deleteTask(${task.id})">Excluir</button>
                <button class="btn btn-edit" onclick="editTask(${task.id})">Editar</button>
            </div>
        `;
        taskList.appendChild(li);
    });
}

// 3. CRIAR TAREFA (POST)
async function createTask(event) {
    event.preventDefault();

    const titleInput = document.getElementById('title');
    const descriptionInput = document.getElementById('description');

    const editingId = event.target.dataset.editingId;

    const payload = {
        title: titleInput.value,
        description: descriptionInput.value
    };

    try {
        let response;

        if (editingId) {
            response = await fetch(`${API_URL}/${editingId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        } else {
            response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        }

        if (response.ok) {
            titleInput.value = '';
            descriptionInput.value = '';

            delete event.target.dataset.editingId;

            document.getElementById('btn-add').textContent = 'Adicionar Tarefa';

            loadTasks();
        } else {
            const err = await response.json();
            alert(err.error || 'Erro ao salvar tarefa');
        }
    } catch (error) {
        console.error('Erro ao salvar:', error);
    }
}

// 4. ATUALIZAR STATUS (PUT)
async function toggleTask(id, completedStatus) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ completed: completedStatus })
        });

        if (response.ok) {
            loadTasks();
        }
    } catch (error) {
        console.error('Erro ao atualizar:', error);
    }
}

// 5. EXCLUIR TAREFA (DELETE)
async function deleteTask(id) {
    const modal = document.getElementById('confirm-modal');
    const confirmYes = document.getElementById('confirm-yes');
    const confirmNo = document.getElementById('confirm-no');

    modal.style.display = 'flex';

    confirmNo.onclick = () => {
        modal.style.display = 'none';
    };

    confirmYes.onclick = async () => {
        modal.style.display = 'none';

        try {
            const response = await fetch(`${API_URL}/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                loadTasks();
            }
        } catch (error) {
            console.error('Erro ao excluir:', error);
        }
    };
}

// Utilitário para evitar XSS
function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Editar Tarefa
function editTask(id) {
    const task = tasks.find(task => task.id === id);

    if (!task) return;

    document.getElementById('title').value = task.title;
    document.getElementById('description').value = task.description || '';

    const form = document.getElementById('task-form');

    form.dataset.editingId = id;

    document.getElementById('btn-add').textContent = 'Salvar Alterações';
}