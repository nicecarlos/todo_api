from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)


# Página inicial: login
@web_bp.route("/")
def index():
    return render_template("login.html")


# Página de tarefas
@web_bp.route("/tasks")
def tasks():
    return render_template("index.html")