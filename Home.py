import streamlit as st
from datetime import date
from funcionario import Funcionario
from cargos import Cargo
from empresas import Empresa
from exames import Exame
from utils import ao_mudar_cargo, cpf_validate

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

    cargo = st.selectbox(
        "Selecione o Cargo",
        opcoes_cargo,
        format_func=lambda x: x.nome if isinstance(x, Cargo) else x,
        key="cargo",
        on_change=ao_mudar_cargo,
        args=(todos_exames, )
    )
    exames_necessarios_ids = st.session_state.get("exames_necessarios_ids", set())

    with st.expander("Exames Necessários", expanded=True):
        exames_selecionados = []
        col_a, col_b = st.columns(2)

        with col_a:
            with st.container(border=True):
                for exame in todos_exames[::2]:
                    is_checked = exame.id in exames_necessarios_ids
                    selecionado = st.checkbox(
                        exame.nome,
                        value=is_checked,
                        key=f"check_esq_{exame.id}"
                    )
                    if selecionado:
                        data_realizacao = st.date_input(
                            "Data de Realização",
                            value=None,
                            format="DD/MM/YYYY",
                            key=f"data_esq_{exame.id}",
                            min_value="1900-01-01",
                            max_value="2999-12-31"
                        )
                        exames_selecionados.append({
                            "exame": exame,
                            "data_realizacao": data_realizacao
                        })
                    st.divider()

        with col_b:
            with st.container(border=True):
                for exame in todos_exames[1::2]:
                    is_checked = exame.id in exames_necessarios_ids
                    selecionado = st.checkbox(
                        exame.nome,
                        value=is_checked,
                        key=f"check_dir_{exame.id}"
                    )
                    if selecionado:
                        data_realizacao = st.date_input(
                            "Data de Realização",
                            value=None,
                            format="DD/MM/YYYY",
                            key=f"data_dir_{exame.id}",
                            min_value="1900-01-01",
                            max_value="2999-12-31"
                        )
                        exames_selecionados.append({
                            "exame": exame,
                            "data_realizacao": data_realizacao
                        })
                    st.divider()

    empresa = st.selectbox("Selecione a empresa", opcoes_empresa, format_func=lambda x: x.razao_social if isinstance(x, Empresa) else x)
    tipo_de_exame = st.selectbox('Selecione o tipo de exame',['Admissional', 'Demissional', 'Periódico', 'Mudança de Risco', 'Retorno ao Trabalho', 'Avaliação Clínica'])

    submitted = st.button("Gerar kit")

    if submitted:
        if not exames_selecionados:
            st.warning("Selecione ao menos um exame para gerar o kit.")
        if not cpf_validate(cpf):
            st.warning("CPF inválido. Verifique e tente novamente.")
        else:
            funcionario = Funcionario(
                nome=nome,
                cpf=cpf,
                data_nascimento=data_nascimento,
                cargo=cargo,
                empresa=empresa,
                sexo=sexo,
                exames_selecionados=exames_selecionados
            )
            pdf_bytes = funcionario.gerar_kit(tipo_de_exame)

            nome_pdf = f"kit_{funcionario.nome.replace(' ', '_')}_{funcionario.cpf[-4:]}.pdf"

            st.download_button(
                label="Baixar Kit de Documentos",
                data=pdf_bytes,
                file_name=nome_pdf,
                mime="application/pdf"
            )