class ProdutoDomain:
    def __init__(self, name, preco, quantidade, status, imagem):
        self.name = name
        self.preco = preco
        self.quantidade = quantidade
        self.status = status
        self.imagem = imagem

        #ajustar imagem.
        
    def to_dict(self):
        return {
            "name": self.name,
            "preço": self.preco,
            "quantidade": self.quantidade,
            "status": self.status,  
            "imagem": self.imagem
        }
    
