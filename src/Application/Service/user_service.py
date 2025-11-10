import random
import os
from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 
from twilio.rest import Client
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from src.Infrastructure.http.whats_app import send_whatsapp_message

load_dotenv() 

class UserService:
    @staticmethod
    def create_user(name, cnpj, email, celular, password, status=False):
        try:
            # Verificar se usuário já existe
            existing_user = User.query.filter((User.email == email) | (User.cnpj == cnpj)).first()
            if existing_user:
                raise Exception("Email ou CNPJ já cadastrado")

            hashed_password = generate_password_hash(password)
            token = str(random.randint(100000, 999999))

            message_sid = send_whatsapp_message(celular, token)
            if not message_sid:
                raise Exception("Não foi possível enviar a mensagem de confirmação via WhatsApp.")

            new_user = UserDomain(
                name, cnpj, email, celular, hashed_password, status, 
                token=token, confirmed=False
            )

            user = User(
                name=new_user.name,
                cnpj=new_user.cnpj,
                email=new_user.email,
                celular=new_user.celular,
                password=new_user.password,  
                status=new_user.status,
                token=new_user.token,
                confirmed=new_user.confirmed
            )

            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def confirm_user(user_id, token):
        try:
            user = User.query.get(user_id)
            if not user:
                return False

            if user.token == token:
                user.confirmed = True
                user.status = True
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_user(id):
        try:
            return User.query.get(id)
        except Exception as e:
            raise e

    @staticmethod
    def update_user(id, name=None, cnpj=None, email=None, celular=None, password=None, status=None):
        try:
            user = User.query.get(id)   
            if not user:
                return None

            # Verificar se novos dados já existem para outros usuários
            if email and email != user.email:
                existing_email = User.query.filter(User.email == email, User.id != id).first()
                if existing_email:
                    raise Exception("Email já está em uso")

            if cnpj and cnpj != user.cnpj:
                existing_cnpj = User.query.filter(User.cnpj == cnpj, User.id != id).first()
                if existing_cnpj:
                    raise Exception("CNPJ já está em uso")

            if name is not None:
                user.name = name
            if cnpj is not None:
                user.cnpj = cnpj
            if email is not None:
                user.email = email
            if celular is not None:
                user.celular = celular
            if password is not None:
                user.password = generate_password_hash(password)
            if status is not None:
                user.status = status

            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def login_user(email, password):
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                return {"success": False, "message": "Usuário não encontrado"}

            if not user.confirmed:
                return {"success": False, "message": "Conta não confirmada"}

            if not user.status:
                return {"success": False, "message": "Conta inativa"}

            if not check_password_hash(user.password, password):
                return {"success": False, "message": "Senha incorreta"}

            return {"success": True, "message": "Login realizado com sucesso", "user": user}
        except Exception as e:
            raise e