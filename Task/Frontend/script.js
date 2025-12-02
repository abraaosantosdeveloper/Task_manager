const apiUrl = "http://localhost:5000/tarefas";

async function fetchTasks() {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error(`Erro: ${response.status}`);
        const tarefas = await response.json();
        const lista = document.getElementById('tarefas-list');
        lista.innerHTML = '';

        if (tarefas.length === 0) {
            document.getElementById('mensagem-vazia').style.display = 'block';
            return;
        }
        document.getElementById('mensagem-vazia').style.display = 'none';

        tarefas.forEach(tarefa => {
            const status = tarefa.status || "pending";
            const item = document.createElement('li');
            item.className = `task-item status-${status}`;

            const content = document.createElement('div');
            content.className = 'task-content';
            const titulo = document.createElement('strong');
            titulo.textContent = tarefa.title;
            const descricao = document.createElement('p');
            descricao.textContent = tarefa.description || 'Sem descrição.';
            content.append(titulo, descricao);
            item.appendChild(content);

            const actionContainer = document.createElement('div');
            actionContainer.className = 'task-actions';

            // Botão status
            const statusLabels = { pending: "Pendente", in_progress: "Em progresso", completed: "Concluído" };
            const btnStatus = document.createElement('button');
            btnStatus.textContent = statusLabels[status];
            btnStatus.className = `status-btn status-btn-${status}`;
            btnStatus.onclick = () => changeStatus(tarefa.id, status);

            // Botão editar
            const btnEdit = document.createElement('button');
            btnEdit.textContent = "Editar";
            btnEdit.className = "edit-btn";
            btnEdit.onclick = () => editTask(tarefa);

            // Botão excluir
            const btnDelete = document.createElement('button');
            btnDelete.textContent = 'Excluir';
            btnDelete.className = 'delete-btn';
            btnDelete.onclick = () => deleteTask(tarefa.id);

            actionContainer.append(btnStatus, btnEdit, btnDelete);
            item.appendChild(actionContainer);
            lista.appendChild(item);
        });
    } catch (error) {
        console.error(error);
        alert("Erro ao carregar tarefas.");
    }
}

// Adicionar tarefa
async function addTask(event) {
    event.preventDefault();
    const titulo = document.getElementById('titulo').value.trim();
    const descricao = document.getElementById('descricao').value.trim();
    const dialog = document.getElementById('Dialog_AddTask');
    if (!titulo) return alert("Título é obrigatório.");

    try {
        await fetch(apiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: titulo, description: descricao, status: "pending" })
        });
        dialog.close();
        document.getElementById('form-tarefa').reset();
        fetchTasks();
    } catch {
        alert("Erro ao adicionar tarefa.");
    }
}

// Alternar status
function changeStatus(id, currentStatus) {
    const nextStatus = { pending: "in_progress", in_progress: "completed", completed: "pending" };
    fetch(`${apiUrl}/${id}/status`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: nextStatus[currentStatus] })
    })
    .then(() => fetchTasks())
    .catch(() => alert("Erro ao alterar status."));
}

// Excluir tarefa
function deleteTask(id) {
    if (!confirm("Deseja excluir esta tarefa?")) return;
    fetch(`${apiUrl}/${id}`, { method: "DELETE" })
        .then(() => fetchTasks())
        .catch(() => alert("Erro ao excluir."));
}

// Editar tarefa
let editTaskId = null;

function editTask(tarefa) {
    editTaskId = tarefa.id;
    document.getElementById("edit-titulo").value = tarefa.title;
    document.getElementById("edit-descricao").value = tarefa.description;
    document.getElementById("Dialog_EditTask").showModal();
}

async function updateTask(event) {
    event.preventDefault();
    const titulo = document.getElementById("edit-titulo").value.trim();
    const descricao = document.getElementById("edit-descricao").value.trim();
    if (!titulo) return alert("Título obrigatório.");

    try {
        await fetch(`${apiUrl}/${editTaskId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: titulo, description: descricao })
        });
        document.getElementById("Dialog_EditTask").close();
        fetchTasks();
    } catch {
        alert("Erro ao atualizar tarefa.");
    }
}
