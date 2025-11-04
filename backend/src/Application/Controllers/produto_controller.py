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

        if not name or preco is None or quantidade is None or not imagem:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)

        produto = ProdutoService.create_product(
            name=name,
            preco=preco,
            quantidade=quantidade,
            imagem=imagem,
            status=status
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
            "imagem": produto.imagem
    
        }), 200)            