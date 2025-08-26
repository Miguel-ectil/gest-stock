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

    @staticmethod
    def get_user(id):
        user = User.query.get(id)
        return user

    @staticmethod
    def update_user(id, name, cnpj, email, celular, password, status=False):
        user = User.query.get(id)   
        if not user:
            return None

        if name is not None:
            user.name = name
        if cnpj is not None:
            user.cnpj = cnpj
        if email is not None:
            user.email = email
        if celular is not None:
            user.celular = celular
        if password is not None:
            user.password = password
        if status is not None:
            user.status = status

        db.session.commit()
        return UserDomain(name=user.name, cnpj=user.cnpj, email=user.email, celular=user.celular, password=user.password, status=user.status)  
    
