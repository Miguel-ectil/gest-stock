from flask import request, jsonify, make_response
from src.Application.Service.venda_service import VendaService
from src.Application.Utils.auth_utils import token_required

class VendaController:
    @staticmethod
    @token_required
    def create_venda(current_user_id):
        try:
            data = request.get_json()
            if not data:
                return make_response(jsonify({"erro": "Dados JSON inválidos ou não fornecidos"}), 400)

            id_produto = data.get('id_produto')
            quantidade = data.get('quantidade')

            if not id_produto or not quantidade:
                return make_response(jsonify({"erro": "ID do produto e quantidade são obrigatórios"}), 400)

            if quantidade <= 0:
                return make_response(jsonify({"erro": "Quantidade deve ser maior que zero"}), 400)

            venda = VendaService.create_venda(
                id_produto=id_produto,
                id_vendedor=current_user_id,
                quantidade=quantidade
            )

            return make_response(jsonify({
                "mensagem": "Venda realizada com sucesso",
                "venda": venda.to_dict()
            }), 201)
            
        except Exception as e:
            print(f"Erro ao criar venda: {str(e)}")
            return make_response(jsonify({"erro": str(e)}), 400)

    @staticmethod
    @token_required
    def get_venda(current_user_id, id_venda):
        try:
            venda = VendaService.get_venda(id_venda)
            if not venda:
                return make_response(jsonify({"erro": "Venda não encontrada"}), 404)

            if venda.id_vendedor != int(current_user_id):
                return make_response(jsonify({"erro": "Acesso negado"}), 403)

            return make_response(jsonify({
                "venda": venda.to_dict()
            }), 200)
            
        except Exception as e:
            print(f"Erro ao buscar venda: {str(e)}")
            return make_response(jsonify({"erro": "Falha ao buscar venda"}), 500)

    @staticmethod
    @token_required
    def list_vendas_vendedor(current_user_id):
        try:
            vendas = VendaService.list_vendas_by_vendedor(current_user_id)
            
            return make_response(jsonify({
                "vendas": [venda.to_dict() for venda in vendas]
            }), 200)
            
        except Exception as e:
            print(f"Erro ao listar vendas: {str(e)}")
            return make_response(jsonify({"erro": "Falha ao listar vendas"}), 500)

    @staticmethod
    @token_required
    def list_vendas_produto(current_user_id, id_produto):
        try:
            # Aqui dicionar lógica para verificar permissões
            vendas = VendaService.list_vendas_by_produto(id_produto)
            
            return make_response(jsonify({
                "vendas": [venda.to_dict() for venda in vendas]
            }), 200)
            
        except Exception as e:
            print(f"Erro ao listar vendas do produto: {str(e)}")
            return make_response(jsonify({"erro": "Falha ao listar vendas do produto"}), 500)