from database.database_meneger import db, DatabaseManager
from typing import Optional

class Cargo:
    def __init__(
        self,
        nome:str,
        id:Optional[int]=None,
        risco_fisico:Optional[str]=None,
        risco_quimico:Optional[str]=None,
        risco_biologico:Optional[str]=None,
        risco_ergonomico:Optional[str]=None,
        acidente:Optional[str]=None,
        db_manager:DatabaseManager=db
        ):
        self.id = id
        self.nome = nome
        self.risco_fisico = risco_fisico
        self.risco_quimico = risco_quimico
        self.risco_biologico = risco_biologico
        self.risco_ergonomico = risco_ergonomico
        self.acidente = acidente
        self.db = db_manager

    def salvar(self):
        query = """
            INSERT INTO cargos (nome, risco_fisico, risco_quimico, risco_biologico, risco_ergonomico, acidente)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        db.execute_query(query, (
            self.nome,
            self.risco_fisico,
            self.risco_quimico,
            self.risco_biologico,
            self.risco_ergonomico,
            self.acidente
        ))

    @classmethod
    def buscar_por_id(cls, id):
        query = "SELECT * FROM cargos WHERE id = ?"
        response = db.fetch_one(query, (id,))
        if response:
            ...
        return None