from src.Application.Controllers.venda_controller import VendaController
from src.Application.Controllers.user_controller import UserController
from src.Application.Controllers.produto_controller import ProdutoController
from flask import jsonify, make_response, request
from src.Application.Utils.auth_utils import token_required

def init_routes(app):    
    @app.errorhandler(Exception)
    def handle_global_error(error):
        print(f"Erro interno: {str(error)}") 
        return make_response(jsonify({
            "erro": "Erro interno do servidor"
        }), 500)
    
    @app.errorhandler(404)
    def handle_not_found(error):
        return make_response(jsonify({
            "erro": "Endpoint não encontrado"
        }), 404)
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return make_response(jsonify({
            "erro": "Método não permitido"
        }), 405)
    

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
    
    @app.route('/api/products/<int:id_produto>', methods=['GET'])
    def get_product(id_produto):
        return ProdutoController.get_product(id_produto)
    
    @app.route('/api/products', methods=['POST'])
    def create_product():
        return ProdutoController.create_product()
    
    @app.route('/api/products/<int:id_produto>', methods=['PUT'])
    def update_product(id_produto):
            return ProdutoController.update_product(id_produto)
    
    @app.route('/api/products/<int:id_produto>/inactivate', methods=['PATCH'])
    def inactivate_product(id_produto):
        return ProdutoController.inactive_product(id_produto)
    
#---- rotas vendas ----
    @app.route('/api/sales', methods=['POST'])
    @token_required
    def create_sale(current_user_id):
        return VendaController.create_venda(current_user_id)
    
    @app.route('/api/sales/<int:id_venda>', methods=['GET'])
    @token_required
    def get_sale(current_user_id, id_venda):
        return VendaController.get_venda(current_user_id, id_venda)
    
    @app.route('/api/sales/my-sales', methods=['GET'])
    @token_required
    def list_my_sales(current_user_id):
        return VendaController.list_vendas_vendedor(current_user_id)
    
    @app.route('/api/sales/product/<int:id_produto>', methods=['GET'])
    @token_required
    def list_sales_by_product(current_user_id, id_produto):
        return VendaController.list_vendas_produto(current_user_id, id_produto)