from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def register_user():
        data = request.get_json()

        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email')
        celular = data.get('celular')
        password = data.get('password')
        status = data.get(False)  

        if not name or not cnpj or not email or not celular or not password:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)

        user = UserService.create_user(
            name=name,
            cnpj=cnpj,
            email=email,
            celular=celular,
            password=password,
            status=status
        )

        return make_response(jsonify({
            "mensagem": "Usuário salvo com sucesso",
            "usuarios": user.to_dict()
        }), 200)
