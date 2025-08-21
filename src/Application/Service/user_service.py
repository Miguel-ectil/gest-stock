from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 

class UserService:
    @staticmethod
    def create_user(name, cnpj, email, celular, password, status=False):
        new_user = UserDomain(name, cnpj, email, celular, password, status)

        user = User(
            name=new_user.name,
            cnpj=new_user.cnpj,
            email=new_user.email,
            celular=new_user.celular,
            password=new_user.password,
            status=new_user.status
        )

        db.session.add(user)
        db.session.commit()
        return user
