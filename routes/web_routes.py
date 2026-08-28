from flask import Blueprint, render_template

# Blueprint das páginas web
# __name__ informa ao Flask onde este Blueprint está localizado.
web_bp = Blueprint("web", __name__)

# Rota da página inicial.
@web_bp.route("/")
def index():
    return render_template("index.html")

# Rota de tarefas
@web_bp.route("/tasks")
def tasks():
    return {"message":"Lista de tarefas"}