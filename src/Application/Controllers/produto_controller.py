from flask import request, jsonify, make_response
from src.Application.Service.produto_service import ProdutoService

class ProdutoController:
    @staticmethod
    def create_product():
        try:
            data = request.get_json()
            if not data:
                return make_response(jsonify({"erro": "Dados JSON inválidos ou não fornecidos"}), 400)

            name = data.get('name')
            preco = data.get('preco')
            quantidade = data.get('quantidade')
            imagem = data.get('imagem')
            status = data.get('status', True)

            if not name or preco is None or quantidade is None:
                return make_response(jsonify({"erro": "Campos obrigatórios faltando"}), 400)

            id_vendedor = data.get('id_vendedor')

            produto = ProdutoService.create_product(
                name=name,
                preco=preco,
                quantidade=quantidade,
                imagem=imagem,
                status=status,
                id_vendedor=id_vendedor
            )
            return make_response(jsonify({
                "mensagem": "Produto criado com sucesso.",
            }), 201)
        except Exception as e:
            print(f"Erro ao criar produto: {str(e)}")
            return make_response(jsonify({"erro": "Falha ao criar produto"}), 500)
    
    @staticmethod
    def get_product(id_produto):
        try:
            produto = ProdutoService.get_product(id_produto)
            if not produto:
                return make_response(jsonify({"erro": "Produto não encontrado"}), 404)

            return make_response(jsonify({
                "id_produto": produto.id_produto,
                "name": produto.name,
                "preco": produto.preco,
                "quantidade": produto.quantidade,
                "status": produto.status, 
                "imagem": produto.imagem,
                "id_vendedor":produto.id_vendedor
            }), 200)
        except Exception as e:
            print(f"Erro ao buscar produto: {str(e)}")
            return make_response(jsonify({"erro": "Falha ao buscar produto"}), 500)

    @staticmethod
    def list_products():
        try:
            produtos = ProdutoService.list_products()
            if not produtos:
                return make_response(jsonify({"erro": "Nenhum produto encontrado"}), 404)
            
            return jsonify([produto.to_dict() for produto in produtos])
        except Exception as e:
            print(f"Erro ao listar produtos: {str(e)}")
            return make_response(jsonify({"erro": "Falha ao listar produtos"}), 500)
    
    @staticmethod
    def update_product(id_produto):
        try:
            data = request.get_json()
            if not data:
                return make_response(jsonify({"erro": "Dados JSON inválidos ou não fornecidos"}), 400)

            name = data.get('name')
            preco = data.get('preco')
            quantidade = data.get('quantidade')
            status = data.get('status')
            imagem = data.get('imagem')

            produto = ProdutoService.update_product(
                id_produto,
                name=name,
                preco=preco,
                quantidade=quantidade,
                status=status,
                imagem=imagem
            )

            if not produto:
                return make_response(jsonify({"erro": "Produto não encontrado"}), 404)

            return make_response(jsonify({
                "mensagem": "Produto atualizado com sucesso.",
                "produto": {
                    "id_produto": produto.id_produto,
                    "name": produto.name,
                    "preco": produto.preco,
                    "quantidade": produto.quantidade,
                    "status": produto.status, 
                    "imagem": produto.imagem,
                    "id_vendedor":produto.id_vendedor
                }
            }), 200)
        except Exception as e:
            print(f"Erro ao atualizar produto: {str(e)}")
            return make_response(jsonify({"erro": "Falha ao atualizar produto"}), 500)
    
    @staticmethod
    def inactive_product(id_produto):
        try:
            produto = ProdutoService.inactive_product(id_produto)
            if not produto:
                return make_response(jsonify({"erro": "Produto não encontrado"}), 404)

            return make_response(jsonify({
                "mensagem": "Produto inativado com sucesso.",
            }), 200)
        except Exception as e:
            print(f"Erro ao inativar produto: {str(e)}")
            return make_response(jsonify({"erro": "Falha ao inativar produto"}), 500)