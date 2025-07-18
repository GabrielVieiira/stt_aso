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

    def add_parecer(self):
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
        self.ln()
    
    def add_observacoes(self):
        altura = 4.3
        self.set_font("Verdana", "B", 8)
        self.set_fill_color(237, 237, 237)
        self.cell(self.largura, altura, "Observações", 1, True, "L", True)

        self.set_font("Verdana", "", 8)
        self.multi_cell(self.largura, altura, " "*400, 1, 'L')
        self.ln(15)
    
    def add_final_section(self, funcionario):
        colaborador_nome = funcionario.nome

        medico_info = [
            "___________________________",
            "Médico / CRM",
            "____/____/________",
        ]
        
        colabrador_info = [
            "___________________________",
            f"{colaborador_nome}",
            f"____/____/________",
        ]
        
        altura = 5
        
        for i in range(0, len(medico_info)):
            posicao_y = self.get_y()
            posicao_x = self.get_x()+self.largura/2
            self.multi_cell(self.largura/2, altura, medico_info[i], False, align='L')
            self.set_xy(posicao_x, posicao_y)
            self.multi_cell(self.largura/2, altura, colabrador_info[i], False, align='L')

    def create_pdf(self, funcionario, tipo_de_exame:str, nome_arquivo:str):
        self.add_page()
        self.add_company_section()
        self.add_employee_section(funcionario)
        self.add_doctor_section()
        self.add_risks_section(funcionario.cargo)
        self.add_tipo_exame(tipo_de_exame)
        self.add_exam_section(funcionario.cargo.exames_necessarios)
        self.add_parecer()
        self.add_observacoes()
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
        if self.page_no() == 1:
            altura = 15
            self.image('logo_teca.png', 10, 13, 33)
            self.set_font("Verdana", "B", 10)
            self.cell(self.largura, altura, "FICHA CLÍNICA",1,True,"C")
            self.ln(1)

    def footer(self):
        self.set_y(-15)
        self.set_font("Verdana", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    def add_title(self, titulo, alinhamento="C"):
        self.set_font("Verdana", "B", 9)
        self.set_fill_color(237, 237, 237)
        self.cell(self.largura, 6, titulo, 1, ln=True, fill=True, align=alinhamento)

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
        self.add_title("Questionário do Funcionário")
        self.ln(2)

        linha = '___________________________________________'
        perguntas_acientes_pessoais = [
            f"1. Tem ou já teve algum tipo de doença / traumatismo?  [ ] Sim  [ ] Não \n Descreva:{linha}",
            f"2. Já passou por cirurgias?  [ ] Sim  [ ] Não \n Descreva:{linha}",
            f"3. Faz uso de algum tipo de medicação?  [ ] Sim  [ ] Não \n Qual?{linha}",
        ]
        
        perguntas_antecedentes_profissionais = [
            f"4. Nome da empresa (último emprego):{linha}",
            f"5. Cargo:{linha}",
            f"6. Tempo de serviço:{linha}",
            f"7. Desenvolveu alguma doença ocupacional (relacionada ao trabalho)?  [ ] Sim  [ ] Não \n Qual?{linha}",
            f"8. Sofreu acidente de trabalho?  [ ] Sim  [ ] Não \n Descreva:{linha}",
        ]
        
        perguntas_antecedentes_familiares = [
            f"9. Antecedentes Familiares (Hipertensão, Diabetes, etc):{linha}",
            f"10. Causa mortis (pais, irmãos, filhos):{linha}",
        ]
        
        perguntas_habitos = [
            f"11. Você fuma?  [ ] Sim  [ ] Não [ ] Ex fumante \n Quantos por dia?{linha}",
            f"12. Usa bebidas alcoólicas?  [ ] Sim  [ ] Não \n Frequência:{linha}",
            f"13. Pratica atividade física?  [ ] Sim  [ ] Não \n Frequência:{linha}"
        ]
        
        perguntas_inss = [
            f"14. Já recebeu auxílio previdenciário?  [ ] Sim  [ ] Não \n Duração:{linha}"
        ]
        
        perguntas = perguntas_acientes_pessoais + perguntas_antecedentes_profissionais + perguntas_antecedentes_familiares + perguntas_habitos + perguntas_inss
        self.set_font("Verdana", "", 8)
        self.multiline_box("\n".join(perguntas), altura=5)
        
        self.cell(0, 6, "Declaro que as informações acima são verdadeiras.", ln=True)
        self.cell(0, 8, "Assinatura do(a) Candidato(a): ______________________________", ln=True)

    def add_ficha_clinica_medico(self):
        self.add_page()
        self.add_title("Questionário para preenchimento do(a) Médico(a) Examinador(a)")
        self.ln(2)
        linha = '___________________________________________'
        perguntas = [
            f'Estado psicológico: [ ] Calmo [ ] Agitado [ ] Estressado [ ] Ansioso [ ] Deprimido [ ] Outros \n {linha}',
            f"Possui fobias?  [ ] Sim  [ ] Não \n Quais?{linha}",
            f"Está com a vacinação em dia? [ ]Sim [ ]Não \n Quais vacinas: [ ] Dupla Adulto [ ] Hepatite B [ ] Influenza [ ] Febre Amarela [ ] Covid [ ] Outros \n {linha}",    
        ]
        self.multiline_box("\n".join(perguntas), altura=5)

        self.add_title("Anamnese / Avaliação Clínica:")
        
        avaliacoes = [
            f"Cabeça e pescoço: \n [ ] Normal [ ] Alterado \n Descreva:{linha*3}",
            f"Pele e mucosas: \n [ ] Normal [ ] Alterado \n Descreva:{linha*3}",
            f"Aparelho cardiovascular: \n [ ] Normal [ ] Alterado \n Descreva:{linha*3}",
            f"Abdômen: \n [ ] Normal [ ] Alterado \n Descreva:{linha*3}",
            f"Aparelho respiratório: \n [ ] Normal [ ] Alterado \n Descreva:{linha*3}",
            f"Membros superiores: \n [ ] Normal [ ] Alterado \n Descreva:{linha*3}",
            f"Membros inferiores: \n [ ] Normal [ ] Alterado \n Descreva:{linha*3}",
            f"Coluna: \n [ ] Normal [ ] Alterado \n Descreva:{linha*3}"
        ]
        
        self.set_font("Verdana", "", 8)
        altura = 5

        for i in range(0, len(avaliacoes), 2):
            posicao_y = self.get_y()
            posicao_x = self.get_x()+self.largura/2
            self.multi_cell(self.largura/2, altura, avaliacoes[i], 1, align='L')
            if i + 1 < len(avaliacoes):
                self.set_xy(posicao_x, posicao_y)
                self.multi_cell(self.largura/2, altura, avaliacoes[i+1], 1, align='L')

    def add_conclusao(self):
        self.add_title("Conclusão do Exame")
        linhas = [
            "Data do Atendimento: ____/____/________",
            "Parecer: ___________________________",
            "Observações:______________________________________________________________________________________________________________________",
             "Assinatura e carimbo do Médico Examinador: ___________________________"
        ]
        self.multiline_box("\n".join(linhas), altura=5)

    def create_pdf(self, nome_arquivo="aso_ficha_clinica.pdf"):
        self.add_page()
        self.add_dados_funcionario()
        self.add_exames_realizados(self.cargo.exames_necessarios)
        self.add_sinais_vitais()
        self.add_ficha_clinica_funcionario()
        self.add_ficha_clinica_medico()
        self.add_conclusao()
        self.output(nome_arquivo)
