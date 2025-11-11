from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
from src.Application.Utils.auth_utils import generate_token

class UserController:
    @staticmethod
    def register_user(): 
        try:
            data = request.get_json()

            name = data.get('name')
            cnpj = data.get('cnpj')
            email = data.get('email') 
            celular = data.get('celular') 
            password = data.get('password')
            status = data.get('status', False) 

            if not name or not cnpj or not email or not celular or not password: 
                return make_response(jsonify({"erro": "Campos obrigatórios faltando"}), 400) 

            user = UserService.create_user(
                name=name,
                cnpj=cnpj,
                email=email,
                celular=celular,
                password=password,
                status=status
            )

            return make_response(jsonify({
                "mensagem": "Usuário criado com sucesso.",
            }), 201)
        except Exception as e:
            print(f"Erro no registro: {str(e)}")
            return make_response(jsonify({"erro": "Falha ao criar usuário"}), 500)

    @staticmethod
    def confirm_user():
        try:
            data = request.get_json()

            user_id = data.get('id')
            token = data.get('token')

            confirmed = UserService.confirm_user(user_id, token)

            if confirmed:
                return make_response(jsonify({
                    "mensagem": "Usuário confirmado com sucesso",
                }), 200)
            else:
                return make_response(jsonify({"erro": "Token inválido ou usuário não encontrado"}), 400)
        except Exception as e:
            print(f"Erro na confirmação: {str(e)}")
            return make_response(jsonify({"erro": "Falha ao confirmar usuário"}), 500)

    @staticmethod
    def get_user(id):
        try:
            user = UserService.get_user(id)

            return make_response(jsonify({
                "id": user.id,
                "name": user.name,
                "cnpj": user.cnpj,
                "email": user.email,
                "celular": user.celular,
                "status": user.status,
                "confirmed": user.confirmed
            }), 200)
        except Exception as e:
            print(f"Erro ao buscar usuário: {str(e)}")
            return make_response(jsonify({"erro": "Falha ao buscar usuário"}), 500)

    @staticmethod
    def update_user(id):
        try:
            data = request.get_json()

            name = data.get('name')
            cnpj = data.get('cnpj')
            email = data.get('email')
            celular = data.get('celular')
            password = data.get('password')
            status = data.get('status')

            user = UserService.update_user(
                id=id,
                name=name,  
                cnpj=cnpj,
                email=email,
                celular=celular,
                password=password,
                status=status
            )
            if not user:
                return make_response(jsonify({"erro": "Usuário não encontrado"}), 404)

            return make_response(jsonify({
                "mensagem": "Dados do usuário atualizados com sucesso",
            }), 200)
        except Exception as e:
            print(f"Erro ao atualizar usuário: {str(e)}")
            return make_response(jsonify({"erro": "Falha ao atualizar usuário"}), 500)

    @staticmethod
    def login_user(data):
        try:
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return make_response(jsonify({"erro": "Email e senha são obrigatórios"}), 400)

            response = UserService.login_user(email, password)

            if not response["success"]:
                return make_response(jsonify({"erro": response["message"]}), 401)

            user = response["user"]
            token = generate_token(user.id)

            return make_response(jsonify({
                "mensagem": response["message"],
                "token": token,
                "usuario": {
                    "id": user.id,
                    "nome": user.name,
                }
            }), 200)

        except Exception as e:
            print(f"Erro no login: {str(e)}")
            return make_response(jsonify({"erro": "Falha no login"}), 500)
