from database.database_meneger import db, DatabaseManager
import streamlit as st
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
        self.exames_necessarios = self._buscar_exames_necessarios()

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
        
    def atualizar_riscos(self) -> None:
        query = """
            UPDATE cargos
            SET risco_fisico = ?, risco_quimico = ?, risco_biologico = ?, risco_ergonomico = ?, acidente = ?
            WHERE id = ?
        """
        db.execute_query(query, (
            self.risco_fisico,
            self.risco_quimico,
            self.risco_biologico,
            self.risco_ergonomico,
            self.acidente,
            self.id
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
    
    def _buscar_exames_necessarios(self) -> list[ExameCargo]:
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

    def atualizar_exame_necessario(self, exame_id: int) -> None:
        necessario = st.session_state.get(f"exame_{self.id}_{exame_id}", "")
        frequencia = st.session_state.get(f"freq_{self.id}_{exame_id}", "")
        if not necessario:
                query = """
                    DELETE FROM exames_cargos WHERE cargo_id = ? AND exame_id = ?
                """
                db.execute_query(query, (self.id, exame_id))
                st.session_state[f"exame_{self.id}_{exame_id}"] = False
                st.session_state[f"freq_{self.id}_{exame_id}"] = None
        else:
            if frequencia in [6,12]:
                query = """
                    INSERT INTO exames_cargos (cargo_id, exame_id, frequencia)
                    VALUES (?, ?, ?)
                    ON CONFLICT(cargo_id, exame_id) DO UPDATE SET frequencia = ?
                """
                db.execute_query(query, (self.id, exame_id, frequencia, frequencia))
            else:
                st.error("Frequência inválida. Deve ser 6 ou 12 meses.")
                st.session_state[f"exame_{self.id}_{exame_id}"] = False
        
    def atualizar_frequencia_de_exame(self, exame_id: int) -> None:
        frequencia = st.session_state.get(f"freq_{self.id}_{exame_id}", "")
        if frequencia in [6, 12]:
            query = """
                UPDATE exames_cargos
                SET frequencia = ?
                WHERE cargo_id = ? AND exame_id = ?
            """
            db.execute_query(query, (frequencia, self.id, exame_id))
        else:
            st.error("Frequência inválida. Deve ser 6 ou 12 meses.")