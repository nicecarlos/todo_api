from flask import Flask
from config import Config
from extensions import db
from routes.web_routes import web_bp
from routes.api_routes import api_bp

def create_app():

    # Criando aplicação

    app = Flask(__name__)
    app.config.from_object(Config)

    # Iniciando banco

    db.init_app(app)

    # Registrando

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # Criando tabelas

    with app.app_context():
        from models import task
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5000,host='localhost',debug=True)
