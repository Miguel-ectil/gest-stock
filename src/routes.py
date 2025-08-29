from src.Application.Controllers.user_controller import UserController
from flask import jsonify, make_response

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
    def get_user(id):
        return UserController.get_user(id)
    
    @app.route('/user/<int:id>', methods=['PUT'])
    def update_user(id):
        return UserController.update_user(id)
