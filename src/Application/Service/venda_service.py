from src.Infrastructure.Model.venda import Venda
from src.Infrastructure.Model.produto import Produto
from src.Infrastructure.Model.user import User
from src.config.data_base import db

class VendaService:
    @staticmethod
    def create_venda(id_produto, id_vendedor, quantidade):
        try:
            produto = Produto.query.get(id_produto)
            if not produto:
                raise Exception("Produto não encontrado")
            
            if not produto.status:
                raise Exception("Produto inativo não pode ser vendido")
            
            vendedor = User.query.get(id_vendedor)
            if not vendedor:
                raise Exception("Vendedor não encontrado")
            
            if not vendedor.status:
                raise Exception("Vendedor inativo não pode realizar vendas")
            
            if not vendedor.confirmed:
                raise Exception("Vendedor não confirmado não pode realizar vendas")
            

            if produto.quantidade < quantidade:
                raise Exception(f"Estoque insuficiente. Disponível: {produto.quantidade}")
            
            venda = Venda(
                id_produto=id_produto,
                id_vendedor=id_vendedor,
                quantidade=quantidade,
                preco_unitario=produto.preco
            )
            
            produto.quantidade -= quantidade
            
            db.session.add(venda)
            db.session.commit()
            
            return venda
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_venda(id_venda):
        try:
            return Venda.query.get(id_venda)
        except Exception as e:
            raise e
    
    @staticmethod
    def list_vendas_by_vendedor(id_vendedor):
        try:
            return Venda.query.filter_by(id_vendedor=id_vendedor).all()
        except Exception as e:
            raise e
    
    @staticmethod
    def list_vendas_by_produto(id_produto):
        try:
            return Venda.query.filter_by(id_produto=id_produto).all()
        except Exception as e:
            raise e
    
    @staticmethod
    def list_all_vendas():
        try:
            return Venda.query.all()
        except Exception as e:
            raise e