from models.exame import Exame

def cadastrar_exame(nome, precisa_de_pedido):
    exame = Exame(
        nome=nome,
        precisa_de_pedido=precisa_de_pedido
    )
    try:
        exame.salvar()
        return True, "Exame cadastrado com sucesso."
    except Exception as e:
        return False, f"Erro ao cadastrar exame: {str(e)}"

def buscar_exame_por_id(id):
    return Exame.buscar_por_id(id)