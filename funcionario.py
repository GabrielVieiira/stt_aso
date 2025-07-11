from datetime import datetime, date

class Funcionario:
    def __init__(self, nome:str, cpf:str, data_nascimento:date, data_admissao:date, cargo:str, empresa:str) -> None:
        nome = nome.strip()
        cpf = cpf.strip()
        data_nascimento = data_nascimento
        data_admissao = data_admissao
        cargo = cargo.strip()
        empresa = empresa.strip()
        
        print("Funcionário criado com sucesso!")