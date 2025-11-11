from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.config.data_base import db 

class Produto(db.Model):
    __tablename__ = 'produtos'
    id_produto = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    preco = Column(Float, nullable=False)  # Alterado para Float para permitir preços decimais
    quantidade = Column(Integer, nullable=False)
    status = Column(Boolean, default=True)
    imagem = Column(String(255), nullable=True)
    id_vendedor = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Novos campos básicos
    descricao = Column(String(500), nullable=True)
    categoria = Column(String(255), nullable=True)
    sku = Column(String(100), nullable=True)
    desconto = Column(Float, default=0.0)  # Percentual de desconto, por exemplo

    vendedor = relationship("User", back_populates="produtos")

    def to_dict(self):
        return {
            "id": self.id_produto,
            "name": self.name,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "status": self.status,
            "imagem": self.imagem,
            "id_vendedor": self.id_vendedor,
            "descricao": self.descricao,
            "categoria": self.categoria,
            "sku": self.sku,
            "desconto": self.desconto
        }
