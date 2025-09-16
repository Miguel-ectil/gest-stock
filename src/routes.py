from src.Application.Controllers.user_controller import UserController
from flask import jsonify, make_response, request
from src.Application.Utils.auth_utils import token_required

def init_routes(app):    
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
    
    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()

    @app.route('/user/confirm', methods=['POST'])
    def confirm_user():
        return UserController.confirm_user()
  
    @app.route('/user/<int:id>', methods=['GET'])
    @token_required
    def get_user(current_user_id, id):
        if current_user_id != str(id):
            return make_response(jsonify({"erro": "Acesso negado"}), 403)
        
        return UserController.get_user(id)
    
    @app.route('/user/<int:id>', methods=['PUT'])
    @token_required
    def update_user(current_user_id, id):
        if current_user_id != str(id):
            return make_response(jsonify({"erro": "Acesso negado"}), 403)

        return UserController.update_user(id)
    
    @app.route('/user/login', methods=['POST'])
    def login_user():
        data = request.json 
        return UserController.login_user(data)

