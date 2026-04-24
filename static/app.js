// Base API URL (same origin)
const API = window.location.origin;

// DOM elements
const todoForm = document.getElementById('todo-form');
const titleInput = document.getElementById('title');
const completedInput = document.getElementById('completed');
const todoIdInput = document.getElementById('todo-id');
const submitBtn = document.getElementById('submit-btn');
const cancelEditBtn = document.getElementById('cancel-edit');
const formTitle = document.getElementById('form-title');
const formError = document.getElementById('form-error');
const messageBox = document.getElementById('message');
const todoList = document.getElementById('todo-list');

/** Utility: show temporary info message */
function showMessage(text, type = 'info') {
    messageBox.textContent = text;
    messageBox.className = type === 'error' ? 'error-message' : 'info-message';
    messageBox.classList.remove('hidden');
    setTimeout(() => {
        messageBox.classList.add('hidden');
    }, 3000);
}

/** Utility: display form validation error */
function showFormError(msg) {
    formError.textContent = msg;
    formError.classList.remove('hidden');
}

function clearFormError() {
    formError.textContent = '';
    formError.classList.add('hidden');
}

/** Reset form to Create mode */
function resetForm() {
    todoIdInput.value = '';
    titleInput.value = '';
    completedInput.checked = false;
    submitBtn.textContent = 'Add Todo';
    formTitle.textContent = 'Create New Todo';
    cancelEditBtn.classList.add('hidden');
    clearFormError();
}

/** Populate form for editing */
function populateForm(todo) {
    todoIdInput.value = todo.id;
    titleInput.value = todo.title || '';
    completedInput.checked = !!todo.completed;
    submitBtn.textContent = 'Update Todo';
    formTitle.textContent = 'Edit Todo';
    cancelEditBtn.classList.remove('hidden');
    clearFormError();
}

/** Fetch and render the todo list */
async function loadTodos() {
    try {
        const response = await fetch(`${API}/todos`);
        if (!response.ok) throw new Error(`Failed to fetch todos (status ${response.status})`);
        const todos = await response.json();
        renderTodoList(todos);
    } catch (err) {
        showMessage(err.message, 'error');
    }
}

/** Render list items */
function renderTodoList(todos) {
    // Clear current list
    todoList.innerHTML = '';
    if (!Array.isArray(todos) || todos.length === 0) {
        todoList.innerHTML = '<li>No todos found.</li>';
        return;
    }
    todos.forEach(todo => {
        const li = document.createElement('li');
        li.className = 'todo-item' + (todo.completed ? ' completed' : '');
        li.dataset.id = todo.id;
        li.innerHTML = `
            <div>
                <strong>${escapeHtml(todo.title)}</strong>
            </div>
            <div class="todo-actions">
                <button class="edit" type="button">Edit</button>
                <button class="delete" type="button">Delete</button>
            </div>
        `;
        // Edit button handler
        li.querySelector('.edit').addEventListener('click', () => {
            populateForm(todo);
        });
        // Delete button handler
        li.querySelector('.delete').addEventListener('click', async () => {
            if (!confirm('Delete this todo?')) return;
            try {
                const delResp = await fetch(`${API}/todos/${todo.id}`, {
                    method: 'DELETE'
                });
                if (!delResp.ok) throw new Error(`Delete failed (status ${delResp.status})`);
                showMessage('Todo deleted successfully');
                loadTodos();
            } catch (e) {
                showMessage(e.message, 'error');
            }
        });
        todoList.appendChild(li);
    });
}

/** Simple HTML escaping */
function escapeHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

/** Form submit handler – Create or Update */
todoForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearFormError();
    const title = titleInput.value.trim();
    const completed = completedInput.checked;
    // Client‑side validation
    if (!title) {
        showFormError('Title is required');
        return;
    }
    const payload = { title, completed };
    const isEdit = Boolean(todoIdInput.value);
    const url = isEdit ? `${API}/todos/${todoIdInput.value}` : `${API}/todos`;
    const method = isEdit ? 'PUT' : 'POST';
    try {
        const resp = await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        if (!resp.ok) throw new Error(`${isEdit ? 'Update' : 'Create'} failed (status ${resp.status})`);
        const result = await resp.json();
        showMessage(isEdit ? 'Todo updated' : 'Todo created');
        resetForm();
        loadTodos();
    } catch (err) {
        showMessage(err.message, 'error');
    }
});

/** Cancel edit button */
cancelEditBtn.addEventListener('click', () => {
    resetForm();
});

// Initial load
document.addEventListener('DOMContentLoaded', loadTodos);
