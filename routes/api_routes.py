from flask import Blueprint, request, jsonify, session

from services.task_service import TaskService
from services.user_service import UserService

api_bp = Blueprint("api", __name__)

# ==========================
# ROTA TASKS
# ==========================

@api_bp.route("/tasks", methods=["GET"])
def get_tasks():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "Usuário não autenticado."
        }), 401

    tasks = TaskService.list_all_tasks(user_id)

    return jsonify(tasks), 200


@api_bp.route("/tasks", methods=["POST"])
def create_task():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "Usuário não autenticado."
        }), 401

    data = request.get_json() or {}

    try:
        task = TaskService.create_task(data, user_id)

        return jsonify(task), 201

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400


@api_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "Usuário não autenticado."
        }), 401
    
    data = request.get_json() or {}

    try:
        updated = TaskService.update_task(task_id, data, user_id)
        if not updated:
            return jsonify({"error": "Tarefa não encontrada."}), 404
        return jsonify(updated), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "Usuário não autenticado."
        }), 401

    success = TaskService.delete_task(task_id, user_id)

    if not success:
        return jsonify({"error": "Tarefa não encontrada."}), 404
    return jsonify({"message": "Tarefa excluída com sucesso."}), 200


# ==========================
# ROTA USERS
# ==========================

# CADASTRO
@api_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json() or {}

    try:
        user = UserService.create_user(data)
        return jsonify(user.to_dict()), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# LOGIN
@api_bp.route("/users/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "E-mail e senha são obrigatórios."
        }), 400

    user = UserService.login(email, password)

    if not user:
        return jsonify({
            "error": "E-mail ou senha incorretos."
        }), 401

    session["user_id"] = user.id

    return jsonify({
        "message": "Login realizado com sucesso.",
        "user": user.to_dict()
    }), 200


# LOGOUT
@api_bp.route("/users/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logout realizado com sucesso."}), 200