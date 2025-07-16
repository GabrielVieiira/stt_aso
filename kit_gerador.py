from fpdf import FPDF
import re
from empresas import Empresa
from cargos import Cargo
from exame_cargo_dto import ExameCargo
from datetime import datetime

class AsoGerador(FPDF):

    def __init__(self, empresa_info:Empresa, cargo_info:Cargo)-> None:
        super().__init__()
        self.add_font("Verdana", "", "fonts/verdana.ttf", uni=True)
        self.add_font("Verdana", "B", "fonts/verdanab.ttf", uni=True)
        self.add_font("Verdana", "I", "fonts/verdanai.ttf", uni=True)
        self.empresa_info = empresa_info
        self.riscos = cargo_info
        self.largura = 190

    def header(self):
        altura = 32
        self.image('logo_teca.png', 10, 20, 33)
        self.set_font("Verdana", "B", 10)
        self.cell(self.largura, altura, "ASO - ATESTADO DE SAUDE OCUPACIONAL",1,True,"C")
        self.ln(1)

    def footer(self):
        self.set_y(-15)
        self.set_font("Verdana", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    def add_company_section(self):
        altura = 4.3


        self.set_font("Verdana", "B", 8)
        self.set_fill_color(237, 237, 237)
        self.cell(self.largura, altura, "Empresa",1, True, "L", True)
        self.set_font("Verdana", "", 8)

        razao_social = self.empresa_info.razao_social
        cnpj = self.empresa_info.cnpj
        endereco = f"{self.empresa_info.rua}, {self.empresa_info.numero} {self.empresa_info.complemento}".strip()
        bairro = self.empresa_info.bairro
        cidade = self.empresa_info.municipio
        uf = self.empresa_info.uf
        cep = self.empresa_info.cep
        telefone = self.empresa_info.telefone
        email = self.empresa_info.email


        empresa_info = (
            f'Razão Social: {razao_social}\n'
            f"CNPJ: {cnpj}\n"
            f"Endereço: {endereco}\n"
            f"Bairro: {bairro}\n"
            f"Cidade / UF: {cidade} / {uf}  CEP: {cep}\n"
            f"Telefone: {telefone}  Email: {email}"
        )

        self.multi_cell(self.largura, altura, empresa_info, 1, 'L')

    def add_employee_section(self, funcionario)-> None:
        altura = 4.3
        self.set_font("Verdana", "B", 8)
        self.set_fill_color(237, 237, 237)
        self.cell(self.largura, altura, "Funcionário", 1, True, "L", True)

        self.set_font("Verdana", "", 8)
        nome = funcionario.nome
        # matricula = funcionario.get("matricula", "N/A")
        cpf = funcionario.cpf
        cpf_formatado = re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', cpf)
        sexo = funcionario.sexo
        data_nascimento = (
            funcionario.data_nascimento.strftime("%d/%m/%Y")
            if funcionario.data_nascimento
            else "N/A"
        )
        idade = funcionario.idade
        cargo = funcionario.cargo.nome if funcionario.cargo else "N/A"

        funcionario_info = (
            f"Nome: {nome}\n"
            # f"Código: {matricula}\n"
            f"CPF: {cpf_formatado}\n"
            f"Sexo: {sexo}\n"
            f"Data de Nascimento/Idade: {data_nascimento} / {idade}\n"
            f"Função: {cargo}"
        )

        self.multi_cell(self.largura, altura, funcionario_info, 1, 'L')
        self.ln(1)

    def add_doctor_section(
        self,
    ):
        altura = 4.3
        self.set_font("Verdana", "B", 8)
        self.set_fill_color(237, 237, 237)
        self.cell(self.largura, altura, "Médico Responsável pelo PCMSO" ,1, True, "L", True)

        medico_info = (
            f"Nome: IVAN LUCIO COSTA OLAIA\n"
            f"CRM: 3877PSP\n"
            f"Endereço: Praça 20 de Setembro, 122, Piso Superior\n"
            f"Bairro: Centro\n"
            f"Cidade/UF: Itapeva/SP\n"
            f"Telefone: (15) 3521-4169"

        )
        self.set_font("Verdana", "", 8)
        self.multi_cell(self.largura, altura, medico_info, 1, 'L')
        self.ln(1)

    def add_risks_section(self, cargo:Cargo):

        altura = 5
        self.set_font("Verdana", "B", 8)
        self.set_fill_color(237, 237, 237)
        self.cell(self.largura, altura, "Perigos / Fatores de Risco", 1, True, "L", True)
        self.set_font("Verdana", "", 8)

        riscos_fisicos = cargo.risco_fisico
        riscos_quimicos = cargo.risco_quimico
        riscos_ergonomicos = cargo.risco_ergonomico
        acidentes = cargo.acidente

        riscos = (
            f"Físicos: {riscos_fisicos}\n"
            f"Químicos: {riscos_quimicos}\n"
            f"Ergonômicos: {riscos_ergonomicos}\n"
            f"Acidentes: {acidentes}"
        )

        self.set_font("Verdana", "", 8)
        self.multi_cell(self.largura, altura, riscos, 1, 'L')

    def add_tipo_exame(self,tipo_de_exame:str):
        altura = 4.3
        self.set_font("Verdana", "B", 8)
        self.set_fill_color(237, 237, 237)
        self.multi_cell(self.largura, altura, "EM CUMPRIMENTO ÀS PORTARIAS NºS 3214/78, 3164/82, 12/83, 24/94 E 08/96 NR7 DO MINISTÉRIO DO TRABALHO E EMPREGO PARA FINS DE EXAME:", 1, "L", True)
        self.set_font("Verdana", "", 8)

        self.cell(self.largura, altura, f"{tipo_de_exame}", 1, True, "L")
        self.ln(1)

    def add_exam_section(self, exames:list[ExameCargo]):
        altura = 5
        self.set_font("Verdana", "B", 8)
        self.set_fill_color(237, 237, 237)
        self.cell(self.largura, altura, "Avaliação Clínica e Exames Realizados", 1, True, "L", True)
        self.set_font("Verdana", "", 8)

        exames_str = "\n".join(f"____/____/____ {exame.exame.nome}" for exame in exames)

        self.multi_cell(self.largura, altura, exames_str, 1, 'L')
        self.ln(1)

    def add_final_section(self, funcionario):
        colaborador_nome = funcionario.nome
        colaborador_cpf = re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', funcionario.cpf)
        altura = 4.3
        self.set_font("Verdana", "B", 8)
        self.set_fill_color(237, 237, 237)
        self.cell(self.largura, altura, "Parecer", 1, True, "L", True)

        self.set_font("Verdana", "", 8)

        tamanho_quadrado = 3

        self.cell(self.largura / 4, 6, "Apto:", "LTB")
        y = self.get_y()
        self.rect(20,y+1,tamanho_quadrado,tamanho_quadrado)
        self.cell(self.largura - 47.5 , 6, "Inapto:", "RTB")
        y = self.get_y()
        x = 70
        self.rect(x,y+1,tamanho_quadrado,tamanho_quadrado)
        self.ln(15)

        y = self.get_y() + 3
        tamanho_linha = 50
        x = self.get_x()
        self.line(x, y, x + tamanho_linha, y)


        self.cell(0, 10, 'Médico / CRM', 0, 1, 'L')
        self.ln(10)

        y = self.get_y() + 3
        x = self.get_x()
        self.line(x, y, x + tamanho_linha, y)
        self.cell(0, 10, colaborador_nome, 0, 1, 'L')


    def create_pdf(self, funcionario, tipo_de_exame:str, nome_arquivo:str):
        self.add_page()
        self.add_company_section()
        self.add_employee_section(funcionario)
        self.add_doctor_section()
        self.add_risks_section(funcionario.cargo)
        self.add_tipo_exame(tipo_de_exame)
        self.add_exam_section(funcionario.cargo.exames_necessarios)
        self.add_final_section(funcionario)
        self.output(nome_arquivo)


class FichaClinicaGerador(FPDF):
    def __init__(self, funcionario, empresa, tipo_exame, cargo):
        super().__init__()
        self.funcionario = funcionario
        self.empresa = empresa
        self.tipo_exame = tipo_exame
        self.cargo = cargo
        self.largura = 190

        # Fontes
        self.add_font("Verdana", "", "fonts/verdana.ttf", uni=True)
        self.add_font("Verdana", "B", "fonts/verdanab.ttf", uni=True)
        self.add_font("Verdana", "I", "fonts/verdanai.ttf", uni=True)

    def header(self):
        altura = 32
        self.image('logo_teca.png', 10, 20, 33)
        self.set_font("Verdana", "B", 10)
        self.cell(self.largura, altura, "FICHA CLÍNICA",1,True,"C")
        self.ln(1)

    def footer(self):
        self.set_y(-15)
        self.set_font("Verdana", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    def add_title(self, titulo):
        self.set_font("Verdana", "B", 9)
        self.set_fill_color(237, 237, 237)
        self.cell(self.largura, 6, titulo, 1, ln=True, fill=True)

    def multiline_box(self, texto, altura=4.5, border=True):
        self.set_font("Verdana", "", 8)
        self.multi_cell(self.largura, altura, texto, border)

    def add_dados_funcionario(self):
        self.add_title("Dados do Funcionário")
        nome = self.funcionario.nome
        nascimento = self.funcionario.data_nascimento.strftime("%d/%m/%Y")
        idade = self.funcionario.idade
        sexo = self.funcionario.sexo
        cargo = self.cargo.nome
        admissao = self.funcionario.data_admissao.strftime("%d/%m/%Y")
        tipo_exame = self.tipo_exame
        data_ficha = datetime.today().strftime("%d/%m/%Y")

        texto = (
            f"Nome: {nome}\n"
            f"Empresa: {self.empresa.razao_social}\n"
            f"CNPJ: {self.empresa.cnpj}\n"
            f"Unidade: {self.empresa.razao_social}\n"
            f"Cargo: {cargo}\n"
            f"Sexo: {sexo}  Idade: {idade}  Nascimento: {nascimento}\n"
            f"Admissão: {admissao}   Tipo de Exame: {tipo_exame}   Data Ficha: {data_ficha}\n"
        )
        self.multiline_box(texto)

    def add_exames_realizados(self, exames: list):
        self.add_title("Exames Realizados")
        self.set_font("Verdana", "", 8)

        if not exames:
            self.cell(0, 6, "Nenhum exame informado.", ln=True)
            return

        for exame_cargo in exames:
            nome = exame_cargo.exame.nome
            frequencia = exame_cargo.frequencia or "N/A"
            texto = f"____/____/________ {nome}  (Frequência: {frequencia})"
            self.cell(0, 5, texto, ln=True)

        self.ln(2)

    def add_sinais_vitais(self):
        self.add_title("Sinais Vitais")
        campos = [
            "Temperatura", "Frequência Respiratória (IPM)", "Pressão Arterial (mmHg)",
            "Frequência de Pulso (BPM)", "Altura", "Biotipo", "Peso (Kg)",
            "Índice de Massa Corpórea", "Perímetro Cintura (cm)", "Perímetro Quadril (cm)"
        ]
        texto = "\n".join(f"{campo}: ____________________" for campo in campos)
        self.multiline_box(texto)

    def add_ficha_clinica_funcionario(self):
        self.add_title("Ficha Clínica - Questionário do Funcionário")

        perguntas = [
            "Tem ou já teve algum tipo de doença / traumatismo? Descreva:",
            "Já passou por cirurgias? Descreva:",
            "Faz uso de algum tipo de medicação? Qual?",
            "Nome da empresa (último emprego):",
            "Cargo:",
            "Tempo de serviço:",
            "Desenvolveu alguma doença ocupacional? Qual?",
            "Sofreu acidente de trabalho? Descreva:",
            "Antecedentes Familiares (Hipertensão, Diabetes, etc):",
            "Causa mortis (pais, irmãos, filhos):",
            "Você fuma? Quantos por dia?",
            "Usa bebidas alcoólicas? Frequência:",
            "Pratica atividade física? Frequência:",
            "Já recebeu auxílio previdenciário? Duração:"
        ]
        self.set_font("Verdana", "", 8)
        for pergunta in perguntas:
            self.cell(0, 5, pergunta, ln=True)
            for _ in range(3):
                self.cell(0, 5, "_" * 90, ln=True)
            self.ln(1)

        self.cell(0, 6, "Declaro que as informações acima são verdadeiras.", ln=True)
        self.cell(0, 8, "Assinatura do(a) Candidato(a): ______________________________", ln=True)

    def add_ficha_clinica_medico(self):
        self.add_title("Ficha Clínica - Médico Examinador")

        perguntas = [
            "Estado psicológico (Calmo / Agitado / Estressado / Ansioso / Deprimido):",
            "Possui fobias? Quais:",
            "Está com a vacinação em dia? Quais vacinas:"
        ]
        for pergunta in perguntas:
            self.cell(0, 5, pergunta, ln=True)
            for _ in range(2):
                self.cell(0, 5, "_" * 90, ln=True)
            self.ln(1)

        avaliacoes = [
            "Cabeça e pescoço", "Pele e mucosas", "Aparelho cardiovascular",
            "Abdômen", "Aparelho respiratório", "Membros superiores",
            "Membros inferiores", "Coluna"
        ]
        for campo in avaliacoes:
            self.cell(0, 5, campo + ":", ln=True)
            for _ in range(2):
                self.cell(0, 5, "_" * 90, ln=True)
            self.ln(1)

    def add_conclusao(self):
        self.add_title("Conclusão do Exame")
        self.cell(0, 6, "Data do Atendimento: ____/____/________", ln=True)
        self.cell(0, 6, "Parecer: ___________________________", ln=True)
        self.cell(0, 6, "Observações:", ln=True)
        for _ in range(3):
            self.cell(0, 6, "_" * 90, ln=True)
        self.ln(5)
        self.cell(0, 6, "Assinatura e carimbo do Médico Examinador: ___________________________", ln=True)

    def create_pdf(self, nome_arquivo="aso_ficha_clinica.pdf"):
        self.add_page()
        self.add_dados_funcionario()
        self.add_exames_realizados(self.cargo.exames_necessarios)
        self.add_sinais_vitais()
        # self.add_ficha_clinica_funcionario()
        # self.add_ficha_clinica_medico()
        # self.add_conclusao()
        self.output(nome_arquivo)
