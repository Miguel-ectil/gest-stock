from src.config.data_base import db
from datetime import datetime

class Venda(db.Model):
    __tablename__ = 'vendas'
    
    id_venda = db.Column(db.Integer, primary_key=True)
    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id_produto'), nullable=False)
    id_vendedor = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)
    
    produto = db.relationship('Produto', backref='vendas')
    vendedor = db.relationship('User', backref='vendas')
    
    def to_dict(self):
        return {
            "id_venda": self.id_venda,
            "id_produto": self.id_produto,
            "id_vendedor": self.id_vendedor,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "data_venda": self.data_venda.isoformat() if self.data_venda else None,
            "nome_produto": self.produto.name if self.produto else None,
            "nome_vendedor": self.vendedor.name if self.vendedor else None
        }