from database.database_meneger import db, DatabaseManager
from typing import Optional

class Exame:
    def __init__(self, nome: str, precisa_de_pedido: bool, id: Optional[int]=None, db_manager:DatabaseManager=db):
        self.id = id
        self.nome = nome
        self.precisa_de_pedido = bool(precisa_de_pedido)
        self.db = db_manager

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
    
    def salvar(self):
        if self.id is None:
            query = "INSERT INTO exames (nome, precisa_de_pedido) VALUES (?, ?)"
            db.execute_query(query, (self.nome, self.precisa_de_pedido))
            
    def atualizar(self):
        if self.id is not None:
            query = "UPDATE exames SET nome = ?, precisa_de_pedido = ? WHERE id = ?"
            db.execute_query(query, (self.nome, self.precisa_de_pedido, self.id))
            
    def excluir(self):
        if self.id is not None:
            query = "DELETE FROM exames WHERE id = ?"
            db.execute_query(query, (self.id,))
            self.id = None