from database.database_meneger import db, DatabaseManager
from typing import Optional
from exame_cargo_dto import ExameCargo
from exames import Exame

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
        ) -> None:
        self.id = id
        self.nome = nome
        self.risco_fisico = risco_fisico
        self.risco_quimico = risco_quimico
        self.risco_biologico = risco_biologico
        self.risco_ergonomico = risco_ergonomico
        self.acidente = acidente
        self.db = db_manager

    def salvar(self)-> None:
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
    def buscar_por_id(cls, id) -> Optional['Cargo']:
        query = "SELECT * FROM cargos WHERE id = ?"
        response = db.fetch_one(query, (id,))
        if response:
            ...
        return None
    
    @classmethod
    def listar_todos(cls)-> list['Cargo']:
        query = "SELECT * FROM cargos"
        response = db.fetch_all(query)
        cargos = []
        for row in response:
            cargo = cls(
                id=row['id'],
                nome=row['nome'],
                risco_fisico=row['risco_fisico'],
                risco_quimico=row['risco_quimico'],
                risco_biologico=row['risco_biologico'],
                risco_ergonomico=row['risco_ergonomico'],
                acidente=row['acidente']
            )
            cargos.append(cargo)
        return cargos
    
    def buscar_exames_necessarios(self) -> list[ExameCargo]:
        query = """
            SELECT 
                exames.id,
                exames.nome,
                exames.precisa_de_pedido,
                exames_cargos.frequencia
            FROM exames_cargos
            LEFT JOIN exames
            ON exames_cargos.exame_id = exames.id
            WHERE exames_cargos.cargo_id = ?;"""
        exames_necessarios = db.fetch_all(query, (self.id,))
        return [
            ExameCargo(
                exame=Exame(
                    id=exame['id'],
                    nome=exame['nome'],
                    precisa_de_pedido=exame['precisa_de_pedido']
                ),
                frequencia=exame['frequencia']
            )
            for exame in exames_necessarios
        ]
