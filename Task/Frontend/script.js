const apiUrl = "http://localhost:5000/tarefas";

// FetchTasks é chamado no onload do body do HTML.

// Buscar e listar tarefas
async function fetchTasks() {
    try {
        const response = await fetch(apiUrl);
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
            // VERIFICAÇÃO ADAPTADA: Verifica se o campo status é 'completed'
            const isCompleted = tarefa.status === 'completed'; 
            
            const item = document.createElement('li');
            // Aplica a classe 'completed' se o status for 'completed'
            item.className = isCompleted ? 'task-item completed' : 'task-item'; 

            // Conteúdo da Tarefa
            const content = document.createElement('div');
            content.className = 'task-content';
            
            const titulo = document.createElement('strong');
            titulo.textContent = tarefa.title;

            const descricao = document.createElement('p');
            descricao.textContent = tarefa.description || 'Sem descrição.';
            
            content.appendChild(titulo);
            content.appendChild(descricao);
            item.appendChild(content);

            // Container para os botões
            const actionContainer = document.createElement('div');
            actionContainer.className = 'task-actions';

            // 🟢 Botão Status (Concluído/Pendente)
            const btnComplete = document.createElement('button');
            
            // LÓGICA DE TEXTO E CLASSE ADAPTADA:
            btnComplete.textContent = isCompleted ? 'Concluído' : 'Pendente';
            btnComplete.className = isCompleted ? 'complete-btn completed-status' : 'complete-btn pending-status'; 
            
            btnComplete.onclick = () => completeTask(tarefa.id);

            // ❌ Botão Excluir
            const btnDelete = document.createElement('button');
            btnDelete.textContent = 'Excluir';
            btnDelete.className = 'delete-btn';
            btnDelete.onclick = () => deleteTask(tarefa.id);
            
            actionContainer.appendChild(btnComplete);
            actionContainer.appendChild(btnDelete);
            
            item.appendChild(actionContainer);
            lista.appendChild(item);
        });
    } catch (error) {
        console.error("Erro em fetchTasks:", error);
        alert('Não foi possível carregar as tarefas. Verifique se o servidor está rodando em ' + apiUrl);
    }
}

// Adicionar tarefa
async function addTask(event) {
    event.preventDefault();

    const titulo = document.getElementById('titulo').value.trim();
    const descricao = document.getElementById('descricao').value.trim();
    const dialog = document.getElementById('Dialog_AddTask');

    if (!titulo) {
        alert('Título é obrigatório.');
        return;
    }

    try {
        // Envia a requisição POST
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: titulo, description: descricao })
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Erro ao adicionar tarefa: ${response.status} - ${errorText}`);
        }

        // Limpa o formulário e fecha o diálogo em caso de sucesso
        document.getElementById('form-tarefa').reset();
        dialog.close(); 
        
        fetchTasks();

    } catch (error) {
        console.error("Erro em addTask:", error);
        alert('Não foi possível adicionar a tarefa. Detalhes: ' + error.message);
    }
}

// Concluir/Desfazer tarefa
function completeTask(id) {
    // Note: O endpoint /completar no backend deve saber como alternar o status
    // Se a tarefa estiver 'completed', ele deve mudar para 'pending' (ou vice-versa).
    fetch(`${apiUrl}/${id}/completar`, { method: "PUT" })
      .then(res => { 
          if (!res.ok) throw new Error(`Falha ao alterar status da tarefa. Status: ${res.status}`);
      })
      .then(() => { 
          // Recarrega a lista lendo o NOVO status (completed ou pending) do BD
          fetchTasks(); 
      })
      .catch(err => { 
          console.error(err); 
          alert(err.message || 'Não foi possível alterar o status da tarefa.');
      });
}

// Excluir tarefa
function deleteTask(id) {
    if (!confirm("Tem certeza que deseja excluir esta tarefa?")) {
        return;
    }
    
    fetch(`${apiUrl}/${id}`, { method: "DELETE" })
      .then(res => { 
          if (!res.ok) throw new Error(`Falha ao excluir a tarefa. Status: ${res.status}`);
      })
      .then(() => { 
          fetchTasks(); 
      })
      .catch(err => { 
          console.error(err); 
          alert(err.message || 'Não foi possível excluir a tarefa.');
      });
}