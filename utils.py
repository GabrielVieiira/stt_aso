import streamlit as st
from exames import Exame


def ao_mudar_cargo(todos_exames:list[Exame]):
    cargo_atual = st.session_state.get("cargo")
    if cargo_atual:
        exames_ids = {ec.exame.id for ec in cargo_atual.exames_necessarios}
        st.session_state["exames_necessarios_ids"] = exames_ids

        if not st.session_state.get(f"exames_inicializados_{cargo_atual.id}", False):
            for exame in todos_exames:
                st.session_state[f"check_{exame.id}"] = exame.id in exames_ids
                if f"data_{exame.id}" in st.session_state:
                    del st.session_state[f"data_{exame.id}"]
            st.session_state[f"exames_inicializados_{cargo_atual.id}"] = True
            
        
def cpf_validate(self, cpf):
    #  Obtém os números do CPF e ignora outros caracteres
    cpf = [int(char) for char in cpf if char.isdigit()]

    #  Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
    #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
    if cpf == cpf[::-1]:
        return False

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True