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
    
    def buscar_frequencia(self, cargo_id: int) -> Optional[int]:
        query = "SELECT frequencia FROM exames_cargos WHERE exame_id = ? AND cargo_id = ?"
        response = db.fetch_one(query, (self.id, cargo_id))
        return response['frequencia'] if response else None