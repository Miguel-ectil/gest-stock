class UserDomain:
    def __init__(self, name, cnpj, email, celular, password, status, token=None, confirmed=False):
        self.name = name
        self.cnpj = cnpj
        self.email = email
        self.celular = celular
        self.password = password
        self.status = status
        self.token = token          # token de verificação via WhatsApp
        self.confirmed = confirmed  # status de confirmação (True/False)
    
    def to_dict(self):
        return {
            "name": self.name,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "status": self.status,
             "token": self.token,
            "confirmed": self.confirmed
        }
    
    
