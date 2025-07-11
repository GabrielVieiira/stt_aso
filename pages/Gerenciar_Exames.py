import streamlit as st
from cargos import Cargo
from exames import Exame
from database.database_meneger import db  # supondo que use em algum momento

st.set_page_config(page_title='Home', page_icon="/favicon.ico", layout='wide')

opcoes_cargo = Cargo.listar_todos()
opcoes_exames = Exame.listar_todos()

cargo_selecionado = st.selectbox(
    "Selecione o Cargo",
    opcoes_cargo,
    format_func=lambda x: x.nome if isinstance(x, Cargo) else x
)

exames_necessarios = cargo_selecionado.buscar_exames_necessarios() if cargo_selecionado else []

with st.expander("Editar riscos do cargo"):
    
    # st.subheader(f"Editar riscos do cargo: {cargo_selecionado.nome}")
    with st.form("form_editar_riscos"):
        risco_fisico = st.text_area("Risco Físico:", value=cargo_selecionado.risco_fisico or "")
        risco_quimico = st.text_area("Risco Químico:", value=cargo_selecionado.risco_quimico or "")
        risco_biologico = st.text_area("Risco Biológico:", value=cargo_selecionado.risco_biologico or "")
        risco_ergonomico = st.text_area("Risco Ergonômico:", value=cargo_selecionado.risco_ergonomico or "")
        acidente = st.text_area("Acidente:", value=cargo_selecionado.acidente or "")
        submitted = st.form_submit_button("Atualizar Riscos")
    
with st.expander("Exames necessários para este cargo"):
    exames_selecionados = []
    for exame in opcoes_exames:
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.write(f"🧪 {exame.nome}")
        with col2:
            selecionado = st.checkbox(
                "Necessário?",
                key=f"exame_{cargo_selecionado.id}_{exame.id}",
                value=exame.id in [ec.exame.id for ec in exames_necessarios]
            )
        with col3:
            freq = st.number_input(
                "Frequência",
                value=exame.frequencia if exame.id in [ec.exame.id for ec in exames_necessarios] else None,
                key=f"freq_{cargo_selecionado.id}_{exame.id}")
        
        if selecionado:
            exames_selecionados.append({
                "exame": exame,
                "frequencia": freq
            })

# submitted = st.form_submit_button("Atualizar Cargo")
# if submitted:
#     cargo_selecionado.risco_fisico = risco_fisico
#     cargo_selecionado.risco_quimico = risco_quimico
#     cargo_selecionado.risco_biologico = risco_biologico
#     cargo_selecionado.risco_ergonomico = risco_ergonomico
#     cargo_selecionado.acidente = acidente
#     cargo_selecionado.salvar()

#     db.execute_query("DELETE FROM exames_cargos WHERE cargo_id = ?", (cargo_selecionado.id,))
#     for item in exames_selecionados:
#         exame = item["exame"]
#         frequencia = item["frequencia"]
#         db.execute_query(
#             "INSERT INTO exames_cargos (cargo_id, exame_id, frequencia) VALUES (?, ?, ?)",
#             (cargo_selecionado.id, exame.id, frequencia)
#         )

#     st.success(f"Cargo '{cargo_selecionado.nome}' e exames atualizados com sucesso.")