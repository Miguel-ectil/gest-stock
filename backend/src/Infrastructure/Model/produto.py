from sqlalchemy import Column, Integer, String, Boolean
from src.config.data_base import db 

class Produto(db.Model):
    __tablename__ = 'users'
    id_produto = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    preco = Column(Integer, nullable=False) 
    quantidade = Column(Integer, nullable=False)
    status = Column(Boolean, default=True)
    imagem = Column(String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id_produto,
            "name": self.name,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "status": self.status,
            "imagem": self.imagem

        }