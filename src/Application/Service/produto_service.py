from src.Domain.produto import ProdutoDomain         
from src.Infrastructure.Model.produto import Produto    
from src.config.data_base import db       

class ProdutoService:
    @staticmethod
    def create_product(name, preco, quantidade, imagem, status, id_vendedor):
        produto = Produto(
            name=name,
            preco=preco,
            quantidade=quantidade,
            imagem=imagem,
            status=status,
            id_vendedor=id_vendedor
        )

        db.session.add(produto)
        db.session.commit()
        return produto
    
    @staticmethod
    def get_product(id_produto):
        return Produto.query.get(id_produto)
    
    @staticmethod    
    def update_product(id_produto, name=None, preco=None, quantidade=None, status=None, imagem=None):                       
        produto = Produto.query.get(id_produto)   
        if not produto:
            return None            

        if name is not None:                
            produto.name = name
        if preco is not None:                
            produto.preco = preco
        if quantidade is not None:                
            produto.quantidade = quantidade
        if status is not None:                
            produto.status = status
        if imagem is not None:                
            produto.imagem = imagem

        db.session.commit()        
        return produto

    @staticmethod
    def list_products():
        return Produto.query.all()      

    @staticmethod
    def inactive_product(id):
        produto = Produto.query.get(id)
        if not produto:
            return None

        produto.status = False
        db.session.commit()
        return produto
                           