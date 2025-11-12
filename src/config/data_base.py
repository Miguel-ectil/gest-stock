from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

db = SQLAlchemy()

def init_db(app):
    """
    Inicializa o SQLAlchemy com Flask, conectando ao PostgreSQL do Supabase.
    """
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "❌ A variável de ambiente DATABASE_URL não está definida. "
            "Configure com a URL do Supabase PostgreSQL."
        )

    if "sslmode=" not in database_url:
        database_url += "?sslmode=require"

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    print("💾 Conectado ao banco de dados do Supabase com SSL.")
