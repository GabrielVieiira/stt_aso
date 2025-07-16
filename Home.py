import streamlit as st
from datetime import date
from funcionario import Funcionario
from cargos import Cargo
from empresas import Empresa
import os

st.logo("/logo_teca.png", size='large', icon_image='/favicon.ico')

st.set_page_config(page_title='Home', layout='wide')

opcoes_empresa:list[Empresa] = Empresa.listar_todos()
opcoes_cargo:list[Cargo] = Cargo.listar_todos()

st.title("Gerar Kit")

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

    nome_arquivo = funcionario.gerar_kit()

    if nome_arquivo and os.path.exists(nome_arquivo):
        st.success(f"Kit gerado com sucesso para {funcionario.nome}!")

        with open(nome_arquivo, "rb") as file:
            st.download_button(
                label="📄 Baixar ASO",
                data=file,
                file_name=nome_arquivo,
                mime="application/pdf"
            )

        os.remove(nome_arquivo)
    else:
        st.error("Houve um erro ao gerar o arquivo. Verifique os dados ou tente novamente.")