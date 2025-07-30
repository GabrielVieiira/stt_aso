import streamlit as st
from cargos import Cargo
from exames import Exame
import time

st.set_page_config(page_title='Gerenciar Exames', page_icon= 'favicon.ico', layout='wide')
st.logo("logo_teca.png", size='large', icon_image='favicon.ico')

opcoes_cargo = Cargo.listar_todos()
opcoes_exames = Exame.listar_todos()



tab_gerenciar_cargos, tab_gerenciar_exames, tab_adicionar_cargo = st.tabs(["Gerenciar Cargos", "Gerenciar Exames", "Adicionar Cargo"])
with tab_gerenciar_cargos:
    cargo_selecionado = st.selectbox(
        "Selecione o Cargo",
        opcoes_cargo,
        format_func=lambda x: x.nome if isinstance(x, Cargo) else x
    )

    exames_necessarios = cargo_selecionado.exames_necessarios if cargo_selecionado else []
    
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
           
    with st.expander("Editar riscos do cargo"):
        with st.form("form_editar_riscos"):
            risco_fisico = st.text_area("Risco Físico:", value=cargo_selecionado.risco_fisico or "")
            risco_quimico = st.text_area("Risco Químico:", value=cargo_selecionado.risco_quimico or "")
            risco_biologico = st.text_area("Risco Biológico:", value=cargo_selecionado.risco_biologico or "")
            risco_ergonomico = st.text_area("Risco Ergonômico:", value=cargo_selecionado.risco_ergonomico or "")
            acidente = st.text_area("Acidente:", value=cargo_selecionado.acidente or "")
            botao_atualizar_riscos = st.form_submit_button("Atualizar Riscos")

            if botao_atualizar_riscos:
                cargo_selecionado.risco_fisico = risco_fisico
                cargo_selecionado.risco_quimico = risco_quimico
                cargo_selecionado.risco_biologico = risco_biologico
                cargo_selecionado.risco_ergonomico = risco_ergonomico
                cargo_selecionado.acidente = acidente
                cargo_selecionado.atualizar_riscos()
                st.rerun()             

    with st.expander("Editar Nome do Cargo"):
        novo_nome_cargo = st.text_input("Novo Nome do Cargo:", value=cargo_selecionado.nome if cargo_selecionado else "")
        col1, col2 = st.columns([3, 1])
        botao_atualizar_nome_cargo = col1.button("Atualizar")
        botao_excluir_cargo = col2.button("Excluir Cargo")
        if botao_atualizar_nome_cargo and cargo_selecionado:
            cargo_selecionado.nome = novo_nome_cargo
            cargo_selecionado.atualizar()
            st.success(f"Cargo atualizado para '{novo_nome_cargo}' com sucesso!")
            time.sleep(3)
            st.rerun()
        if botao_excluir_cargo and cargo_selecionado:
            cargo_selecionado.excluir()
            st.success(f"Cargo '{cargo_selecionado.nome}' excluído com sucesso!")
            del cargo_selecionado
            time.sleep(3)
            st.rerun()

with tab_gerenciar_exames:
    with st.expander("Adicionar Exame"):
        with st.form("form_adicionar_exame"):
            novo_exame_nome = st.text_input("Nome do Exame:")
            novo_exame_precisa_de_pedido = st.checkbox("Precisa de Pedido Médico?")
            botao_adicionar_exame = st.form_submit_button("Adicionar Exame")

            if botao_adicionar_exame and novo_exame_nome:
                novo_exame = Exame(nome=novo_exame_nome, precisa_de_pedido=novo_exame_precisa_de_pedido)
                novo_exame.salvar()
                st.success(f"Exame '{novo_exame_nome}' adicionado com sucesso!")
                st.rerun()            
    with st.expander("Editar Exames"):
        exame_selecionado = st.selectbox(
            "Selecione o Exame",
            opcoes_exames,
            format_func=lambda x: x.nome if isinstance(x, Exame) else x
        )
        
        with st.container(border=True):
            if exame_selecionado:
                novo_nome = st.text_input("Nome do Exame:", value=exame_selecionado.nome)
                precisa_de_pedido = st.checkbox("Precisa de Pedido Médico?", value=exame_selecionado.precisa_de_pedido)
                col1, col2 = st.columns([3, 1])
                botao_atualizar_exame = col1.button("Atualizar Exame")
                botao_excluir_exame = col2.button("Excluir Exame")

                if botao_atualizar_exame:
                    exame_selecionado.nome = novo_nome
                    exame_selecionado.precisa_de_pedido = precisa_de_pedido
                    exame_selecionado.atualizar()
                    st.success(f"Exame: '{novo_nome}' atualizado com sucesso!")
                    time.sleep(3)
                    st.rerun()
                    
                if botao_excluir_exame:
                    exame_selecionado.excluir()
                    st.success(f"Exame: '{exame_selecionado.nome}' excluído com sucesso!")
                    time.sleep(3)
                    st.rerun()
            
with tab_adicionar_cargo:
    with st.expander("Adicionar Cargo"):
        with st.form("form_adicionar_cargo"):
            novo_cargo_nome = st.text_input("Nome do Cargo:")
            novo_cargo_risco_fisico = st.text_area("Risco Físico:")
            novo_cargo_risco_quimico = st.text_area("Risco Químico:")
            novo_cargo_risco_biologico = st.text_area("Risco Biológico:")
            novo_cargo_risco_ergonomico = st.text_area("Risco Ergonômico:")
            novo_cargo_acidente = st.text_area("Acidente:")
            botao_adicionar_cargo = st.form_submit_button("Adicionar Cargo")

            if botao_adicionar_cargo and novo_cargo_risco_fisico:
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
