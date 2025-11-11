from src.Domain.produto import ProdutoDomain         
from src.Infrastructure.Model.produto import Produto    
from src.config.data_base import db       

class ProdutoService:
    @staticmethod
    def create_product(name, preco, quantidade, imagem=None, status=True, id_vendedor=None,
                       descricao=None, categoria=None, sku=None, desconto=None):
        """
        Cria um produto com campos básicos adicionais.
        """
        try:
            produto = Produto(
                name=name,
                preco=preco,
                quantidade=quantidade,
                imagem=imagem,
                status=status,
                id_vendedor=id_vendedor,
                descricao=descricao,
                categoria=categoria,
                sku=sku,
                desconto=desconto
            )

            db.session.add(produto)
            db.session.commit()
            return produto
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_product(id_produto):
        try:
            return Produto.query.get(id_produto)
        except Exception as e:
            raise e
    
    @staticmethod    
    def update_product(id_produto, name=None, preco=None, quantidade=None, status=None, imagem=None,
                       descricao=None, categoria=None, sku=None, desconto=None):                       
        try:
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
            if descricao is not None:
                produto.descricao = descricao
            if categoria is not None:
                produto.categoria = categoria
            if sku is not None:
                produto.sku = sku
            if desconto is not None:
                produto.desconto = desconto

            db.session.commit()        
            return produto
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def list_products():
        try:
            return Produto.query.all()
        except Exception as e:
            raise e     

    @staticmethod
    def inactive_product(id):
        try:
            produto = Produto.query.get(id)
            if not produto:
                return None

            produto.status = False
            db.session.commit()
            return produto
        except Exception as e:
            db.session.rollback()
            raise e
