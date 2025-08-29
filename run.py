from flask import Flask
from src.config.data_base import init_db, db
from src.routes import init_routes
from src.Infrastructure.Model.user import User  # Caminho corrigido do seu model

def create_app():
    """
    Função que cria e configura a aplicação Flask.
    """
    app = Flask(__name__)
    init_db(app)
    init_routes(app)
    return app

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0', port=8000)