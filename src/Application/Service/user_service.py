import random
import os
from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv() 

class UserService:
    @staticmethod
    def create_user(name, cnpj, email, celular, password, status=False):
       
        token = str(random.randint(100000, 999999))
        
        new_user = UserDomain(name, cnpj, email, celular, password, status, token=token, confirmed=False)
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

       
        UserService.send_whatsapp_token(user.celular, token)  #<- envia o token pelo zap

        return user

    @staticmethod
    def send_whatsapp_token(user_phone, token):
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        content_sid = os.getenv("TWILIO_CONTENT_SID")
        from_number = os.getenv("TWILIO_FROM_NUMBER")

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_=from_number,
            content_sid=content_sid,
            content_variables=f'{{"1":"{token}"}}',
            to=f'whatsapp:{user_phone}'
        )

        return message.sid

    @staticmethod
    def confirm_user(user_id, token):
        user = User.query.get(user_id)
        if not user:
            return None

        if user.token == token:
            user.confirmed = True
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_user(id):
        return User.query.get(id)

    @staticmethod
    def update_user(id, name=None, cnpj=None, email=None, celular=None, password=None, status=None):
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
        return user
