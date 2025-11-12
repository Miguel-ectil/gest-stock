class ProdutoDomain:
    def __init__(self, id_produto=None, name=None, preco=None, quantidade=None,
                 imagem=None, status=True, id_vendedor=None,
                 descricao=None, categoria=None, sku=None, desconto=None):
        self.id_produto = id_produto
        self.name = name
        self.preco = preco
        self.quantidade = quantidade
        self.imagem = imagem
        self.status = status
        self.id_vendedor = id_vendedor
        self.descricao = descricao
        self.categoria = categoria
        self.sku = sku
        self.desconto = desconto

    def to_dict(self):
        """
        Converte o objeto de domínio para um dicionário.
        """
        return {
            "id_produto": self.id_produto,
            "name": self.name,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "imagem": self.imagem,
            "status": self.status,
            "id_vendedor": self.id_vendedor,
            "descricao": self.descricao,
            "categoria": self.categoria,
            "sku": self.sku,
            "desconto": self.desconto
        }

    @staticmethod
    def from_model(produto_model):
        """
        Converte um objeto do modelo (SQLAlchemy) para o domínio.
        """
        return ProdutoDomain(
            id_produto=produto_model.id_produto,
            name=produto_model.name,
            preco=produto_model.preco,
            quantidade=produto_model.quantidade,
            imagem=produto_model.imagem,
            status=produto_model.status,
            id_vendedor=produto_model.id_vendedor,
            descricao=getattr(produto_model, 'descricao', None),
            categoria=getattr(produto_model, 'categoria', None),
            sku=getattr(produto_model, 'sku', None),
            desconto=getattr(produto_model, 'desconto', None)
        )