from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def register_user(): #<---- criar regras para não permitir cadastro duplicado (FERNANDO)
        data = request.get_json()

        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email') 
        celular = data.get('celular') #<--- criar regra para o numero de celular fixcar no padrão (FERNANDO) ex. +5511987404871 tem que começar com +55 e 9 dígitos
        password = data.get('password') #<--- criar regra para senha forte (FERNANDO) ex. no mínimo 8 caracteres, uma letra maiúscula, uma minúscula, um número e um caractere especial
        status = data.get('status', False) 

        if not name or not cnpj or not email or not celular or not password: #<--- fazer o tratamento de erros (FERNANDO) ex. cnpj tem que ser 14 dígitos ou email tem que ser um email válido ou numero de celular não digitado...
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
            "mensagem": "Usuário criado com sucesso. Token enviado via WhatsApp",
            "usuario": {
                "id": user.id, #<--- o ID deve ser UUID 
                "name": user.name,
                "cnpj": user.cnpj,
                "email": user.email,
                "celular": user.celular,
                "status": user.status,
                "confirmed": user.confirmed
            }
        }), 201)

    @staticmethod
    def confirm_user():
        data = request.get_json()

        user_id = data.get('id')
        token = data.get('token')

        if not user_id or not token:
            return make_response(jsonify({"erro": "ID e token são obrigatórios"}), 400)

        confirmed = UserService.confirm_user(user_id, token)

        if confirmed:
            return make_response(jsonify({
                "mensagem": "Usuário confirmado com sucesso",
            }), 200)
        else:
            return make_response(jsonify({"erro": "Token inválido ou usuário não encontrado"}), 400)


    @staticmethod
    def get_user(id):
        user = UserService.get_user(id)
        if not user:
            return make_response(jsonify({"erro": "Usuário não encontrado"}), 404)

        return make_response(jsonify({
            "id": user.id,
            "name": user.name,
            "cnpj": user.cnpj,
            "email": user.email,
            "celular": user.celular,
            "status": user.status,
            "confirmed": user.confirmed
        }), 200)

    @staticmethod
    def update_user(id): #<--- fazer tratamento de erros (FERNANDO) 
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
