from database.database_meneger import db
from typing import Optional

class Exame:
    def __init__(self, id: int, nome: str, precisa_de_pedido: bool):
        self.id = id
        self.nome = nome
        self.precisa_de_pedido = bool(precisa_de_pedido)

    @classmethod
    def listar_todos(cls):
        query = "SELECT * FROM exames"
        response = db.fetch_all(query)
        exames = []
        for row in response:
            exame = cls(
                id=row['id'],
                nome=row['nome'],
                precisa_de_pedido=row['precisa_de_pedido']
            )
            exames.append(exame)
        return exames