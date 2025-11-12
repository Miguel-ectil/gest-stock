from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Inicializa o SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """
    Inicializa a base de dados com o app Flask e o SQLAlchemy.
    Usa o PostgreSQL do Supabase se a variável DATABASE_URL estiver configurada,
    caso contrário, utiliza SQLite local como fallback.
    """
    load_dotenv()

    # Pegar a URL do Supabase
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        # Supabase exige SSL
        if "?sslmode=" not in database_url:
            database_url += "?sslmode=require"
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
        print("💾 Conectado ao banco de dados do Supabase com SSL.")
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        sqlite_path = os.path.join(basedir, '../../database.sqlite')
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{sqlite_path}"
        print("💾 Usando banco de dados SQLite local (modo desenvolvimento).")


    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
