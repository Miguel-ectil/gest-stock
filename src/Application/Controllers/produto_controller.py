from flask import request, jsonify, make_response
from src.Application.Service.produto_service import ProdutoService


class ProdutoController:
    @staticmethod
    def create_product():
        data = request.get_json()

        name = data.get('name')
        preco = data.get('preco')
        quantidade = data.get('quantidade')
        imagem = data.get('imagem')
        status = data.get('status', True)

        if not name or preco is None or quantidade is None:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)

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
    
    @staticmethod
    def get_product(id_produto):
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

    @staticmethod
    def list_products():
        produtos = ProdutoService.list_products()
        if not produtos:
            return make_response(jsonify({"erro": "Nenhum produto encontrado"}), 404)
        
        return jsonify([produto.to_dict() for produto in produtos])
    
    @staticmethod
    def update_product(id_produto):
        data = request.get_json()

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
    
    @staticmethod
    def inactive_product(id_produto):
        produto = ProdutoService.inactive_product(id_produto)
        if not produto:
            return make_response(jsonify({"erro": "Produto não encontrado"}), 404)

        return make_response(jsonify({
            "mensagem": "Produto inativado com sucesso.",
           
            }), 200)
    
    