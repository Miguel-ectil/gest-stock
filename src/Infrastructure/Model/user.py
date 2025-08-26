from sqlalchemy import Column, Integer, String, Boolean
from src.config.data_base import db 
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    cnpj = Column(String(18), nullable=False)  # Adicionado
    email = Column(String(255), nullable=False)
    celular = Column(String(20), nullable=False)  # Adicionado
    password = Column(String(255), nullable=False)
    status = Column(Boolean, default=False)
    token = Column(String(6), nullable=True)       # novo campo para token
    confirmed = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
