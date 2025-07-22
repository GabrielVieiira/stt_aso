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