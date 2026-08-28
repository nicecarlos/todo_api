from flask import Blueprint

# Blueprint da API com prefixo /api
api_bp = Blueprint("api", __name__)

from flask import Blueprint, request, jsonify
from services.task_service import TaskService

api_bp = Blueprint("api", __name__)

# Rotas de Tasks
@api_bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = TaskService.list_all_tasks()
    return jsonify(tasks), 200

@api_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json() or {}
    try:
        new_task = TaskService.create_task(data)
        return jsonify(new_task), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json() or {}
    try:
        updated = TaskService.update_task(task_id, data)
        if not updated:
            return jsonify({"error": "Tarefa não encontrada."}), 404
        return jsonify(updated), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    success = TaskService.delete_task(task_id)
    if not success:
        return jsonify({"error": "Tarefa não encontrada."}), 404
    return jsonify({"message": "Tarefa excluída com sucesso."}), 200