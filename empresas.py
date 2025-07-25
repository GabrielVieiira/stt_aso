from database.database_meneger import db

class Empresa:
    def __init__(
        self,
        id:int,
        razao_social:str,
        rua:str,
        numero:str,
        complemento:str,
        bairro:str,
        municipio:str,
        cep:str,
        uf:str,
        telefone:str,
        email:str,
        cnpj:str
        ):
        self.id = id
        self.razao_social = razao_social
        self.rua = rua
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.municipio = municipio
        self.cep = cep
        self.uf = uf
        self.telefone = telefone
        self.email = email
        self.cnpj = cnpj

    @classmethod
    def listar_todos(cls):
        query = "SELECT * FROM empresas"
        response = db.fetch_all(query)
        empresas = []
        for row in response:
            empresa = cls(
                id=row['id'],
                razao_social=row['razao_social'],
                rua=row['rua'],
                numero=row['numero'],
                complemento=row['complemento'],
                bairro=row['bairro'],
                municipio=row['municipio'],
                cep=row['cep'],
                uf=row['uf'],
                telefone=row['telefone'],
                email=row['email'],
                cnpj=row['cnpj']
            )
            empresas.append(empresa)
        return empresas