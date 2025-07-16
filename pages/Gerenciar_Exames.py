import streamlit as st
from cargos import Cargo
from exames import Exame

st.set_page_config(page_title='Gerenciar Exames', page_icon= 'favicon.ico', layout='wide')
st.logo("logo_teca.png", size='large', icon_image='favicon.ico')

opcoes_cargo = Cargo.listar_todos()
opcoes_exames = Exame.listar_todos()

cargo_selecionado = st.selectbox(
    "Selecione o Cargo",
    opcoes_cargo,
    format_func=lambda x: x.nome if isinstance(x, Cargo) else x
)

exames_necessarios = cargo_selecionado.exames_necessarios if cargo_selecionado else []
with st.expander("Editar riscos do cargo"):

    with st.form("form_editar_riscos"):
        risco_fisico = st.text_area("Risco Físico:", value=cargo_selecionado.risco_fisico or "")
        risco_quimico = st.text_area("Risco Químico:", value=cargo_selecionado.risco_quimico or "")
        risco_biologico = st.text_area("Risco Biológico:", value=cargo_selecionado.risco_biologico or "")
        risco_ergonomico = st.text_area("Risco Ergonômico:", value=cargo_selecionado.risco_ergonomico or "")
        acidente = st.text_area("Acidente:", value=cargo_selecionado.acidente or "")
        submitted = st.form_submit_button("Atualizar Riscos")

        if submitted:
            cargo_selecionado.risco_fisico = risco_fisico
            cargo_selecionado.risco_quimico = risco_quimico
            cargo_selecionado.risco_biologico = risco_biologico
            cargo_selecionado.risco_ergonomico = risco_ergonomico
            cargo_selecionado.acidente = acidente
            cargo_selecionado.atualizar_riscos()
            st.rerun()

with st.expander("Exames necessários para este cargo"):
    for exame in opcoes_exames:
        col1, col2, col3 = st.columns([3, 2, 2])
        frequencias_validas = [6, 12]
        frequencia = exame.buscar_frequencia(cargo_selecionado.id)
        with col1:
            st.write(f"🧪 {exame.nome}")
        with col3:
            freq = st.selectbox(
                "Frequência",
                options=frequencias_validas,
                placeholder="Selecione a frequência",
                on_change=cargo_selecionado.atualizar_frequencia_de_exame,
                args=(exame.id,),
                label_visibility="collapsed",
                index=frequencias_validas.index(frequencia) if exame.id in [ec.exame.id for ec in exames_necessarios] and frequencia in frequencias_validas else None,
                key=f"freq_{cargo_selecionado.id}_{exame.id}"
            )
        if freq:
            with col2:
                selecionado = st.checkbox(
                    "Necessário?",
                    key=f"exame_{cargo_selecionado.id}_{exame.id}",
                    on_change=cargo_selecionado.atualizar_exame_necessario,
                    args=(exame.id,),
                    value=exame.id in [ec.exame.id for ec in exames_necessarios]
                )
        st.divider()

        # cargo_selecionado.atualizar_exame_necessario(exame.id)

        # if selecionado:
        #     exames_selecionados.append({
        #         "exame": exame,
        #         "frequencia": freq
        #     })

    # if st.button("Salvar Exames Necessários"):
    #     for exame_info in exames_selecionados:
    #         exame = exame_info["exame"]
    #         frequencia = exame_info["frequencia"]
    #         cargo_selecionado.adicionar_exame(exame, frequencia)
    #     st.success("Exames atualizados com sucesso!")
    #     st.rerun()
        # st.write(st.session_state.get(f"exame_{cargo_selecionado.id}_{exame.id}", ""))
