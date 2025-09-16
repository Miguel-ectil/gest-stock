import jwt
import datetime
from flask import request, jsonify, make_response

# Colocar no .env
SECRET_KEY = "minha_chave_super_secreta"

def generate_token(user_id):
    payload = {
        "user_id": str(user_id),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return make_response(jsonify({"erro": "Token não fornecido"}), 401)

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return make_response(jsonify({"erro": "Formato de token inválido"}), 401)

        payload = decode_token(token)
        if not payload:
            return make_response(jsonify({"erro": "Token inválido ou expirado"}), 401)
        return f(payload["user_id"], *args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper