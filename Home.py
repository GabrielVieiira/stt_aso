import streamlit as st
from datetime import date
from funcionario import Funcionario
from cargos import Cargo
from empresas import Empresa

st.set_page_config(page_title='Home', page_icon="/favicon.ico", layout='wide')
opcoes_empresa = Empresa.listar_todos()
opcoes_cargo = Cargo.listar_todos()

st.title("Cadastro de Funcionário")

with st.form("form_funcionario"):
    nome = st.text_input("Nome do Colaborador")
    cpf = st.text_input("CPF do Colaborador", max_chars=11)
    data_nascimento = st.date_input("Data de nascimento", value=date(1990, 1, 1), format="DD/MM/YYYY")
    data_admissao = st.date_input("Data de Admissão", value=date.today(), format="DD/MM/YYYY")
    cargo = st.selectbox("Selecione o Cargo", opcoes_cargo, format_func=lambda x: x.nome if isinstance(x, Cargo) else x)
    empresa = st.selectbox("Selecione a empresa", opcoes_empresa, format_func=lambda x: x.razao_social if isinstance(x, Empresa) else x)

    submitted = st.form_submit_button("Gerar kit")

    if submitted:
        funcionario = Funcionario(
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            data_admissao=data_admissao,
            cargo=cargo,
            empresa=empresa
        )
        