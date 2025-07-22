import streamlit as st
from cargos import Cargo
from exames import Exame

st.set_page_config(page_title='Gerenciar Exames', page_icon= 'favicon.ico', layout='wide')
st.logo("logo_teca.png", size='large', icon_image='favicon.ico')

opcoes_cargo = Cargo.listar_todos()
opcoes_exames = Exame.listar_todos()



tab1, tab2, tab3 = st.tabs(["Gerenciar Cargos", "Gerenciar Exames", "Editar Riscos do Cargo"])
with tab1:
    cargo_selecionado = st.selectbox(
        "Selecione o Cargo",
        opcoes_cargo,
        format_func=lambda x: x.nome if isinstance(x, Cargo) else x
    )

    exames_necessarios = cargo_selecionado.exames_necessarios if cargo_selecionado else []
    
    with st.expander("Adicionar Cargo"):
        with st.form("form_adicionar_cargo"):
            novo_cargo_nome = st.text_input("Nome do Cargo:")
            novo_cargo_risco_fisico = st.text_area("Risco Físico:")
            novo_cargo_risco_quimico = st.text_area("Risco Químico:")
            novo_cargo_risco_biologico = st.text_area("Risco Biológico:")
            novo_cargo_risco_ergonomico = st.text_area("Risco Ergonômico:")
            novo_cargo_acidente = st.text_area("Acidente:")
            submitted = st.form_submit_button("Adicionar Cargo")

            if submitted and novo_cargo_risco_fisico:
                novo_cargo = Cargo(
                    nome=novo_cargo_nome,
                    risco_fisico=novo_cargo_risco_fisico,
                    risco_quimico=novo_cargo_risco_quimico,
                    risco_biologico=novo_cargo_risco_biologico,
                    risco_ergonomico=novo_cargo_risco_ergonomico,
                    acidente=novo_cargo_acidente
                    )
                novo_cargo.salvar()
                st.success(f"Cargo '{novo_cargo_risco_fisico}' adicionado com sucesso!")
                st.rerun()   
    
    with st.expander("Exames necessários para o cargo selecionado"):
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
            
with tab2:
    with st.expander("Adicionar Exame"):
        with st.form("form_adicionar_exame"):
            novo_exame_nome = st.text_input("Nome do Exame:")
            novo_exame_precisa_de_pedido = st.checkbox("Precisa de Pedido Médico?")
            submitted = st.form_submit_button("Adicionar Exame")

            if submitted and novo_exame_nome:
                novo_exame = Exame(nome=novo_exame_nome, precisa_de_pedido=novo_exame_precisa_de_pedido)
                novo_exame.salvar()
                st.success(f"Exame '{novo_exame_nome}' adicionado com sucesso!")
                st.rerun()            
            
with tab3:
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

