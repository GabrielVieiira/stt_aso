import streamlit as st
from datetime import date
from funcionario import Funcionario
from cargos import Cargo
from empresas import Empresa
import os


st.set_page_config(page_title='Home', page_icon= 'favicon.ico', layout='wide')
st.logo("logo_teca.png", size='large')

opcoes_empresa:list[Empresa] = Empresa.listar_todos()
opcoes_cargo:list[Cargo] = Cargo.listar_todos()

st.title("Gerar Kit")

with st.form("form_funcionario"):
    nome = st.text_input("Nome do Colaborador")
    cpf = st.text_input("CPF do Colaborador", max_chars=11)
    data_nascimento = st.date_input(
        "Data de nascimento",
        value=date(1990, 1, 1),
        format="DD/MM/YYYY",
        min_value="1900-01-01",
        max_value="2999-12-31"
    )
    sexo = st.selectbox('Selecione o sexo',['MASCULINO', 'FEMININO'])
    data_admissao = st.date_input(
        "Data de Admissão",
        value=date.today(),
        format="DD/MM/YYYY",
        min_value="1900-01-01",
        max_value="2999-12-31"
        )
    cargo = st.selectbox("Selecione o Cargo", opcoes_cargo, format_func=lambda x: x.nome if isinstance(x, Cargo) else x)
    empresa = st.selectbox("Selecione a empresa", opcoes_empresa, format_func=lambda x: x.razao_social if isinstance(x, Empresa) else x)
    tipo_de_exame = st.selectbox('Selecione o tipo de exame',['Admissional', 'Demissional', 'Periódico', 'Mudança de Risco', 'Retorno ao Trabalho', 'Avaliação Clínica'])

    submitted = st.form_submit_button("Gerar kit")

if submitted:
    st.write(data_nascimento)
    st.write(data_admissao)
    funcionario = Funcionario(
        nome=nome,
        cpf=cpf,
        data_nascimento=data_nascimento,
        data_admissao=data_admissao,
        cargo=cargo,
        empresa=empresa,
        sexo= sexo
    )

    nome_arquivo_ficha_clinica, nome_arquivo_aso = funcionario.gerar_kit(tipo_de_exame)

    if nome_arquivo_aso and os.path.exists(nome_arquivo_aso):
        st.success(f"ASO gerado com sucesso para {funcionario.nome}!")

    if nome_arquivo_ficha_clinica and os.path.exists(nome_arquivo_ficha_clinica):
        st.success(f"Ficha Clinica gerado com sucesso para {funcionario.nome}!")

        with open(nome_arquivo_aso, "rb") as file:
            st.download_button(
                label="📄 Baixar ASO",
                data=file,
                file_name=nome_arquivo_aso,
                mime="application/pdf"
            )
        with open(nome_arquivo_ficha_clinica, "rb") as file:
            st.download_button(
                label="📄 Baixar Ficha Clinica",
                data=file,
                file_name=nome_arquivo_ficha_clinica,
                mime="application/pdf"
            )

        os.remove(nome_arquivo_aso)
        os.remove(nome_arquivo_ficha_clinica)
    else:
        st.error("Houve um erro ao gerar o arquivo. Verifique os dados ou tente novamente.")
