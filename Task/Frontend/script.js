const apiUrl = "http://localhost:5000/tarefas";

document.addEventListener("DOMContentLoaded", function() {
  fetchTasks();
});

let taskForm = document.getElementById("task-form");
let taskList = document.getElementById("task-list");

// Função para carregar tarefas da API
const API_URL = 'http://localhost:5000/tarefas';

// Buscar e listar tarefas
async function fetchTasks() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error(`Erro ao buscar tarefas: ${response.status}`);

        const tarefas = await response.json();
        const lista = document.getElementById('tarefas-list');
        lista.innerHTML = '';

        if (tarefas.length === 0) {
            document.getElementById('mensagem-vazia').style.display = 'block';
            return;
        } else {
            document.getElementById('mensagem-vazia').style.display = 'none';
        }

        tarefas.forEach(tarefa => {
            const item = document.createElement('li');

            // Título em negrito
            const titulo = document.createElement('strong');
            titulo.textContent = tarefa.title;

            // Descrição abaixo
            const descricao = document.createElement('p');
            descricao.textContent = tarefa.description || '';

            item.appendChild(titulo);
            item.appendChild(descricao);

            lista.appendChild(item);
        });
    } catch (error) {
        console.error(error);
        alert('Não foi possível carregar as tarefas.');
    }
}

// Adicionar tarefa
async function addTask(event) {
    event.preventDefault();

    const titulo = document.getElementById('titulo').value.trim();
    const descricao = document.getElementById('descricao').value.trim();

    if (!titulo) {
        alert('Título é obrigatório.');
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: titulo, description: descricao })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.erro || 'Erro ao adicionar tarefa.');
        }

        document.getElementById('form-tarefa').reset();
        fetchTasks();

    } catch (error) {
        console.error(error);
        alert('Não foi possível adicionar a tarefa.');
    }
}

// Evento do formulário
document.getElementById('form-tarefa').addEventListener('submit', addTask);

// Carregar tarefas ao iniciar
window.addEventListener('DOMContentLoaded', fetchTasks);



// Concluir tarefa
function completeTask(id) {
  fetch(apiUrl + "/" + id + "/completar", { method: "PUT" })
    .then(function(res) { return res.json(); })
    .then(function() { fetchTasks(); })
    .catch(function(err) { console.error(err); });
}

// Excluir tarefa
function deleteTask(id) {
  fetch(apiUrl + "/" + id, { method: "DELETE" })
    .then(function(res) { return res.json(); })
    .then(function() { fetchTasks(); })
    .catch(function(err) { console.error(err); });
}
