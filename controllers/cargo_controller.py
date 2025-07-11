from models.cargo import Cargo

def cadastrar_cargo(
    nome,
    risco_fisico,
    risco_quimico,
    risco_biologico,
    risco_ergonomico,
    acidente
    ):
    cargo = Cargo(
        nome=nome,
        risco_fisico=risco_fisico,
        risco_quimico=risco_quimico,
        risco_biologico=risco_biologico,
        risco_ergonomico=risco_ergonomico,
        acidente=acidente
    )
    try:
        cargo.salvar()
        return True, "Cargo cadastrado com sucesso."
    except Exception as e:
        return False, f"Erro ao cadastrar cargo: {str(e)}"

def buscar_cargo_por_id(id):
    return Cargo.buscar_por_id(id)