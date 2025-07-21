import streamlit as st
from datetime import date
from funcionario import Funcionario
from cargos import Cargo
from empresas import Empresa
from exames import Exame
import os


st.set_page_config(page_title='Home', page_icon= 'favicon.ico', layout='wide')
st.logo("logo_teca.png", size='large')

opcoes_empresa:list[Empresa] = Empresa.listar_todos()
opcoes_cargo:list[Cargo] = Cargo.listar_todos()
todos_exames = Exame.listar_todos()

st.markdown("<h1 style='text-align: center;'>Gerar Kit</h1>", unsafe_allow_html=True)

with st.container(border=True):
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
    exames_necessarios_ids = {exame_cargo.exame.id for exame_cargo in cargo.exames_necessarios}
    with st.expander("Exames Necessários", expanded=True):
        exames_selecionados = []
        for exame in todos_exames:
            is_checked = exame.id in exames_necessarios_ids
            col1, col2 = st.columns([2, 1])
            selecionado = col1.checkbox(exame.nome, value=is_checked, key=f"check_{exame.id}")
            if selecionado:
                data_realizacao = col2.date_input(
                    label="Data de Realização",
                    value=None,
                    format="DD/MM/YYYY",
                    key=f"data_{exame.id}",
                    min_value="1900-01-01",
                    max_value="2999-12-31"
                    )
                exames_selecionados.append({
                    "exame": exame,
                    "data_realizacao": data_realizacao
                })
            else:
                data_realizacao = None

    empresa = st.selectbox("Selecione a empresa", opcoes_empresa, format_func=lambda x: x.razao_social if isinstance(x, Empresa) else x)
    tipo_de_exame = st.selectbox('Selecione o tipo de exame',['Admissional', 'Demissional', 'Periódico', 'Mudança de Risco', 'Retorno ao Trabalho', 'Avaliação Clínica'])

    if exames_selecionados:
        submitted = st.button("Gerar kit")
   
if submitted:
    funcionario = Funcionario(
        nome=nome,
        cpf=cpf,
        data_nascimento=data_nascimento,
        data_admissao=data_admissao,
        cargo=cargo,
        empresa=empresa,
        sexo= sexo,
        exames_selecionados=exames_selecionados
    )

    nome_arquivo_ficha_clinica, nome_arquivo_aso, nome_arquivo_encaminhamento_exame = funcionario.gerar_kit(tipo_de_exame)

    if nome_arquivo_aso and os.path.exists(nome_arquivo_aso):
        st.success(f"ASO gerado com sucesso para {funcionario.nome}!")
        with open(nome_arquivo_aso, "rb") as file:
            st.download_button(
                label="📄 Baixar ASO",
                data=file,
                file_name=nome_arquivo_aso,
                mime="application/pdf"
            )         
    else:
        st.error("Houve um erro ao gerar o ASO. Verifique os dados ou tente novamente.")

    if nome_arquivo_ficha_clinica and os.path.exists(nome_arquivo_ficha_clinica):
        st.success(f"Ficha Clinica gerado com sucesso para {funcionario.nome}!")
        with open(nome_arquivo_ficha_clinica, "rb") as file:
            st.download_button(
                label="📄 Baixar Ficha Clinica",
                data=file,
                file_name=nome_arquivo_ficha_clinica,
                mime="application/pdf"
            )
      
    else:
        st.error("Houve um erro ao gerar o Ficha Clinica. Verifique os dados ou tente novamente.")
      
    if nome_arquivo_encaminhamento_exame and os.path.exists(nome_arquivo_encaminhamento_exame):
        st.success(f"Encaminhamento de exame gerado com sucesso para {funcionario.nome}!")
        with open(nome_arquivo_encaminhamento_exame, "rb") as file:
            st.download_button(
                label="📄 Baixar Encaminhamento de Exame",
                data=file,
                file_name=nome_arquivo_encaminhamento_exame,
                mime="application/pdf"
            )

        os.remove(nome_arquivo_aso)
        os.remove(nome_arquivo_ficha_clinica)
        os.remove(nome_arquivo_encaminhamento_exame)
    else:
        st.error("Houve um erro ao gerar o Encaminhamento de exame. Verifique os dados ou tente novamente.")
