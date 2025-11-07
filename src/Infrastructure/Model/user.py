from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.config.data_base import db 
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    cnpj = Column(String(18), nullable=False) 
    email = Column(String(255), nullable=False)
    celular = Column(String(20), nullable=False)  
    password = Column(String(255), nullable=False)
    status = Column(Boolean, default=False)
    token = Column(String(6), nullable=True)      
    confirmed = Column(Boolean, default=False)

    produtos = relationship("Produto", back_populates="vendedor")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
