from src.Application.Controllers.user_controller import UserController
from src.Application.Controllers.produto_controller import ProdutoController
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


#---- rotas produtos ----
    @app.route('/api/products', methods=['GET'])
    def list_products():

        return ProdutoController.list_products()
    
    @app.route('/api/products/<int:id>', methods=['GET'])
    def get_product(id_produto):
        return ProdutoController.get_product(id_produto)
    
    @app.route('/api/products', methods=['POST'])
    def create_product():
        return ProdutoController.create_product()
    
    @app.route('/api/products/<int:id>', methods=['PUT'])
    def update_product(id_produto):
        if current_user_id != str(id_produto):
            return ProdutoController.update_product(id_produto)
    
    @app.route('/api/products/<int:id>/inactivate', methods=['PATCH'])
    def inactivate_product(id_produto):
        return ProdutoController.inactivate_product(id_produto)
