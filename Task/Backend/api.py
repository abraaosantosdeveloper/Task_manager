from flask import Flask, request, jsonify
from flask_cors import CORS
from Repository import Repository

app = Flask(__name__)
CORS(app)

repository = Repository()  # instancia o repositório

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    try:
        tarefas = repository.get_all()  # deve retornar lista de dicionários
        return jsonify(tarefas)
    except Exception as e:
        # Retorna erro detalhado no console
        print("Erro ao listar tarefas:", e)
        return jsonify({"erro": "Não foi possível listar tarefas"}), 500

@app.route('/tarefas', methods=['POST'])
def adicionar_tarefa():
    data = request.get_json()
    titulo = data.get('title')
    descricao = data.get('description', '')
    if not titulo:
        return jsonify({"erro": "Título é obrigatório"}), 400
    repository.add(titulo, descricao)
    return jsonify({"mensagem": "Tarefa adicionada com sucesso"}), 201

@app.route('/tarefas/<int:task_id>', methods=['DELETE'])
def excluir_tarefa(task_id):
    repository.delete(task_id)
    return jsonify({"mensagem": "Tarefa excluída"}), 200

@app.route('/tarefas/<int:task_id>/status', methods=['PUT'])
def atualizar_status(task_id):
    data = request.get_json()
    status = data.get('status')
    if status not in ['pending', 'in_progress', 'completed']:
        return jsonify({"erro": "Status inválido"}), 400
    repository.update_status(task_id, status)
    return jsonify({"mensagem": "Status atualizado"}), 200

@app.route('/tarefas/<int:task_id>/completar', methods=['PUT'])
def completar_tarefa(task_id):
    repository.complete(task_id)
    return jsonify({"mensagem": "Tarefa marcada como concluída"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)