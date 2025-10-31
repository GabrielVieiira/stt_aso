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
            
        
def cpf_validate(cpf):
    cpf = [int(char) for char in cpf if char.isdigit()]

    if len(cpf) != 11:
        return False

    if cpf == cpf[::-1]:
        return False

    for i in range(9, 11):
        value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True