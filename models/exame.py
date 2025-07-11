from database.database_meneger import db, DatabaseManager

class Exame:
    def __init__(
        self,
        id:int,
        nome:str,
        precisa_de_pedido:int,
        db_manager=db
        ):
        self.id = id
        self.nome = nome
        self.precisa_de_pedido = bool(precisa_de_pedido)
        self.db = db_manager

    def salvar(self):
        query = "INSERT INTO exames (nome, precisa_de_pedido) VALUES (?, ?)"
        db.execute_query(query, (self.nome, self.precisa_de_pedido))

    @classmethod
    def buscar_por_id(cls, id):
        query = "SELECT * FROM exames WHERE id = ?"
        response = db.fetch_one(query, (id,))
        if response:
            ...
        return None