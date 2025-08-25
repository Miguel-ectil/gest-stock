class UserDomain:
    def __init__(self, name, cnpj, email, celular, password, status):
        self.name = name
        self.cnpj = cnpj
        self.email = email
        self.celular = celular
        self.password = password
        self.status = status
    
    def to_dict(self):
        return {
            "name": self.name,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "status": self.status
            # ⚠️ Atenção: evite retornar a senha por segurança
        }
