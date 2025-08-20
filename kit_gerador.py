from fpdf import FPDF
import re
from empresas import Empresa
from datetime import datetime

class AsoGerador:
    def __init__(self, pdf: FPDF, funcionario, empresa_info: Empresa, tipo_de_exame: str) -> None:
        self.pdf = pdf
        self.empresa_info = empresa_info
        self.funcionario = funcionario
        self.tipo_de_exame = tipo_de_exame
        self.largura = 190

        self.pdf.add_font("Verdana", "", "fonts/verdana.ttf", uni=True)
        self.pdf.add_font("Verdana", "B", "fonts/verdanab.ttf", uni=True)
        self.pdf.add_font("Verdana", "I", "fonts/verdanai.ttf", uni=True)

    def header(self):
        altura = 15
        self.pdf.set_y(1)
        self.pdf.image('logo_teca.png', 10, 4, 33)
        self.pdf.set_font("Verdana", "B", 10)
        self.pdf.cell(self.largura, altura, "ASO - ATESTADO DE SAUDE OCUPACIONAL",1,True,"C")
        self.pdf.ln(1)

    # def footer(self):
    #     self.pdf.set_y(-15)
    #     self.pdf.set_font("Verdana", "I", 8)
    #     self.pdf.cell(0, 10, f"Página {self.pdf.page_no()}", 0, 0, "C")
        
    def add_title(self, titulo:str, alinhamento:str="C", altura:float=4):
        self.pdf.set_font("Verdana", "B", 9)
        self.pdf.set_fill_color(237, 237, 237)
        self.pdf.multi_cell(self.largura, altura, titulo, border=1, align=alinhamento, fill=True)

    def multiline_box(self, texto, altura=4.5, border=True):
        self.pdf.set_font("Verdana", "", 8)
        self.pdf.multi_cell(self.largura, altura, texto, border)

    def add_company_section(self):
        altura = 4.3

        self.add_title('Empresa', 'L')
        self.pdf.set_font("Verdana", "", 8)

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

        self.pdf.multi_cell(self.largura, altura, empresa_info, 1, 'L')

    def add_employee_section(self,)-> None:
        altura = 4.3
        self.add_title('Funcionário', 'L')

        self.pdf.set_font("Verdana", "", 8)
        nome = self.funcionario.nome
        # matricula = funcionario.get("matricula", "N/A")
        cpf = self.funcionario.cpf
        cpf_formatado = re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', cpf)
        sexo = self.funcionario.sexo
        data_nascimento = (
            self.funcionario.data_nascimento.strftime("%d/%m/%Y")
            if self.funcionario.data_nascimento
            else "N/A"
        )
        idade = self.funcionario.idade
        cargo = self.funcionario.cargo.nome if self.funcionario.cargo else "N/A"

        funcionario_info = (
            f"Nome: {nome}\n"
            # f"Código: {matricula}\n"
            f"CPF: {cpf_formatado}\n"
            f"Sexo: {sexo}\n"
            f"Data de Nascimento/Idade: {data_nascimento} / {idade}\n"
            f"Função: {cargo}"
        )

        self.pdf.multi_cell(self.largura, altura, funcionario_info, 1, 'L')
        self.pdf.ln(1)

    def add_doctor_section(
        self,
    ):
        altura = 4.3
        self.add_title('Médico Responsável pelo PCMSO', 'L')

        medico_info = (
            f"Nome: IVAN LUCIO COSTA OLAIA\n"
            f"CRM: 3877PSP\n"
            f"Endereço: Praça 20 de Setembro, 122, Piso Superior\n"
            f"Bairro: Centro\n"
            f"Cidade/UF: Itapeva/SP\n"
            f"Telefone: (15) 3521-4169"

        )
        self.pdf.set_font("Verdana", "", 8)
        self.pdf.multi_cell(self.largura, altura, medico_info, 1, 'L')
        self.pdf.ln(1)

    def add_risks_section(self,):

        altura = 5
        self.add_title('Perigos / Fatores de Risco', 'L')
        riscos_fisicos = self.funcionario.cargo.risco_fisico if self.funcionario.cargo.risco_fisico else "N/A"
        riscos_quimicos = self.funcionario.cargo.risco_quimico
        riscos_biologicos = self.funcionario.cargo.risco_biologico
        riscos_ergonomicos = self.funcionario.cargo.risco_ergonomico
        acidentes = self.funcionario.cargo.acidente

        riscos = (
            f"Físicos: {riscos_fisicos}\n"
            f"Químicos: {riscos_quimicos}\n"
            f"Biológicos: {riscos_biologicos}\n"
            f"Ergonômicos: {riscos_ergonomicos}\n"
            f"Acidentes: {acidentes}"
        )

        self.pdf.set_font("Verdana", "", 8)
        self.pdf.multi_cell(self.largura, altura, riscos, 1, 'L')

    def add_tipo_exame(self,):
        altura = 4.3
        self.add_title("EM CUMPRIMENTO ÀS PORTARIAS NºS 3214/78, 3164/82, 12/83, 24/94 E 08/96 NR7 DO MINISTÉRIO DO TRABALHO E EMPREGO PARA FINS DE EXAME:", 'L', altura)
        self.pdf.set_font("Verdana", "", 8)

        self.pdf.cell(self.largura, altura, f"{self.tipo_de_exame}", 1, True, "L")
        self.pdf.ln(1)

    def add_tabela_de_exames(self):
        self.add_title('Avaliação Clínica e Exames Realizados', 'L')
        
        cabecalho = [
            ("DATA", 0.25),
            ("EXAME", 0.25),
            ("DATA", 0.25),
            ("EXAME", 0.25),
        ]
        
        self.pdf.set_font("Verdana", "B", 8)
        for nome_coluna, proporcao in cabecalho:
            tamanho_coluna = self.largura * proporcao
            self.pdf.cell(tamanho_coluna, 6, nome_coluna, 1, 0, "C")
            
        self.pdf.ln()
    
    def add_exam_section(self):
        altura = 5
        self.add_tabela_de_exames()
        self.pdf.set_font("Verdana", "", 8)

        exames = sorted(self.funcionario.exames_selecionados, key=lambda x: x["exame"].nome.lower())
        largura_coluna = self.largura * 0.25

        def render_exame(exame):
            data = exame.get("data_realizacao")
            data_str = data.strftime("%d/%m/%Y") if data else ""
            nome = exame["exame"].nome
            self.pdf.cell(largura_coluna, altura, data_str, 1,align='C')
            self.pdf.cell(largura_coluna, altura, nome, 1,align='C')

        i = 0
        while i < len(exames):
            render_exame(exames[i])
            
            if i + 1 < len(exames):
                render_exame(exames[i + 1])
            else:
                self.pdf.cell(largura_coluna, altura, "", 1,align='C')
                self.pdf.cell(largura_coluna, altura, "", 1,align='C')

            self.pdf.ln()
            i += 2

        self.pdf.ln(1)

    def add_parecer(self):
        self.add_title("Parecer do Médico", 'L')

        self.pdf.set_font("Verdana", "", 8)

        tamanho_quadrado = 3

        self.pdf.cell(self.largura / 4, 6, "Apto:", "LTB")
        y = self.pdf.get_y()
        self.pdf.rect(20,y+1,tamanho_quadrado,tamanho_quadrado)
        self.pdf.cell(self.largura - 47.5 , 6, "Inapto:", "RTB")
        y = self.pdf.get_y()
        x = 70
        self.pdf.rect(x,y+1,tamanho_quadrado,tamanho_quadrado)
        self.pdf.ln(8)
    
    def add_final_section(self):
        colaborador_nome = self.funcionario.nome

        medico_info = [
            "___________________________",
            "      Médico / CRM",
            "     ____/____/________",
        ]
        
        colabrador_info = [
            "___________________________",
            f"{colaborador_nome}",
            f"   ____/____/________",
        ]
        
        altura = 5
        
        for i in range(0, len(medico_info)):
            posicao_y = self.pdf.get_y()
            posicao_x = self.pdf.get_x()+self.largura/2
            self.pdf.multi_cell(self.largura/2, altura, medico_info[i], False, align='L')
            self.pdf.set_xy(posicao_x, posicao_y)
            self.pdf.multi_cell(self.largura/2, altura, colabrador_info[i], False, align='L')

    def gerar(self):
        for _ in range(3):
            self.pdf.add_page()
            self.header()
            self.add_company_section()
            self.add_employee_section()
            self.add_doctor_section()
            self.add_risks_section()
            self.add_tipo_exame()
            self.add_exam_section()
            self.add_parecer()
            self.add_final_section()

class FichaClinicaGerador:
    def __init__(self, pdf: FPDF, funcionario, empresa, tipo_exame, cargo):
        self.pdf = pdf
        self.funcionario = funcionario
        self.empresa = empresa
        self.tipo_exame = tipo_exame
        self.cargo = cargo
        self.largura = 190

        self.pdf.add_font("Verdana", "", "fonts/verdana.ttf", uni=True)
        self.pdf.add_font("Verdana", "B", "fonts/verdanab.ttf", uni=True)
        self.pdf.add_font("Verdana", "I", "fonts/verdanai.ttf", uni=True)

    def header(self):
        altura = 15
        self.pdf.set_y(1)
        self.pdf.image('logo_teca.png', 10, 4, 33)
        self.pdf.set_font("Verdana", "B", 10)
        self.pdf.cell(self.largura, altura, "FICHA CLÍNICA",1,True,"C")
        self.pdf.ln(1)

    # def footer(self):
    #     self.pdf.set_y(-15)
    #     self.pdf.set_font("Verdana", "I", 8)
    #     self.pdf.cell(0, 10, f"Página {self.pdf.page_no()}", 0, 0, "C")
    
    def add_title(self, titulo, alinhamento="C"):
        self.pdf.set_font("Verdana", "B", 9)
        self.pdf.set_fill_color(237, 237, 237)
        self.pdf.cell(self.largura, 6, titulo, 1, ln=True, fill=True, align=alinhamento)

    def multiline_box(self, texto, altura=4.5, border=True):
        self.pdf.set_font("Verdana", "", 8)
        self.pdf.multi_cell(self.largura, altura, texto, border)

    def add_dados_funcionario(self):
        self.add_title("Dados do Funcionário")
        nome = self.funcionario.nome
        cpf = self.funcionario.cpf
        cpf_formatado = re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', cpf)
        nascimento = self.funcionario.data_nascimento.strftime("%d/%m/%Y")
        idade = self.funcionario.idade
        sexo = self.funcionario.sexo
        cargo = self.cargo.nome
        tipo_exame = self.tipo_exame
        data_ficha = datetime.today().strftime("%d/%m/%Y")

        texto = (
            f"Nome: {nome}      CPF: {cpf_formatado}      Tipo de exame: {tipo_exame} \n"
            f"Sexo: {sexo}  Idade: {idade}  Nascimento: {nascimento}\n"
            f"Cargo: {cargo}\n"
            f"Tipo de Exame: {tipo_exame}   Data Ficha: {data_ficha}\n"
            f"Empresa: {self.empresa.razao_social}\n"
            f"CNPJ: {self.empresa.cnpj}\n"
            f"Unidade: {self.empresa.razao_social}\n"
        )
        self.multiline_box(texto)

    def add_exames_realizados(self, exames: list):
        self.add_title("Exames Realizados")
        self.pdf.set_font("Verdana", "", 8)

        if not exames:
            self.pdf.cell(0, 6, "Nenhum exame informado.", ln=True)
            return

        exames_texto = [exame['exame'].nome for exame in exames]
        texto = ", ".join(exames_texto)
        self.pdf.multi_cell(0, 5, texto, True)
        self.pdf.ln(2)

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
        self.pdf.ln(2)

        linha = '___________________________________________'
        perguntas = [
            # Pessoais
            f"1. Tem ou já teve algum tipo de doença / traumatismo?  [ ] Sim  [ ] Não \n Descreva:{linha}",
            f"2. Já passou por cirurgias?  [ ] Sim  [ ] Não \n Descreva:{linha}",
            f"3. Faz uso de algum tipo de medicação?  [ ] Sim  [ ] Não \n Qual?{linha}",
            # Profissionais
            f"4. Nome da empresa (último emprego):{linha}",
            f"5. Cargo:{linha}",
            f"6. Tempo de serviço:{linha}",
            f"7. Desenvolveu alguma doença ocupacional?  [ ] Sim  [ ] Não \n Qual?{linha}",
            f"8. Sofreu acidente de trabalho?  [ ] Sim  [ ] Não \n Descreva:{linha}",
            # Familiares
            f"9. Antecedentes Familiares (Hipertensão, Diabetes, etc):{linha}",
            f"10. Causa mortis (pais, irmãos, filhos):{linha}",
            # Hábitos
            f"11. Você fuma?  [ ] Sim  [ ] Não [ ] Ex fumante \n Quantos por dia?{linha}",
            f"12. Usa bebidas alcoólicas?  [ ] Sim  [ ] Não \n Frequência:{linha}",
            f"13. Pratica atividade física?  [ ] Sim  [ ] Não \n Frequência:{linha}",
            # INSS
            f"14. Já recebeu auxílio previdenciário?  [ ] Sim  [ ] Não \n Duração:{linha}"
        ]

        self.pdf.set_font("Verdana", "", 8)
        self.multiline_box("\n".join(perguntas), altura=5)
        self.pdf.cell(0, 6, "Declaro que as informações acima são verdadeiras.", ln=True)
        self.pdf.cell(0, 8, "Assinatura do(a) Candidato(a): ______________________________", ln=True)

    def add_ficha_clinica_medico(self):
        self.pdf.add_page()
        self.add_title("Questionário para preenchimento do(a) Médico(a) Examinador(a)")
        self.pdf.ln(2)

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

        self.pdf.set_font("Verdana", "", 8)
        altura = 5

        for i in range(0, len(avaliacoes), 2):
            posicao_y = self.pdf.get_y()
            posicao_x = self.pdf.get_x() + self.largura / 2
            self.pdf.multi_cell(self.largura / 2, altura, avaliacoes[i], 1, align='L')
            if i + 1 < len(avaliacoes):
                self.pdf.set_xy(posicao_x, posicao_y)
                self.pdf.multi_cell(self.largura / 2, altura, avaliacoes[i + 1], 1, align='L')

    def add_conclusao(self):
        self.add_title("Conclusão do Exame")
        linhas = [
            "Data do Atendimento: ____/____/________",
            "Parecer: ___________________________",
            "Observações:______________________________________________________________________________________________________________________",
            "Assinatura e carimbo do Médico Examinador: ___________________________"
        ]
        self.multiline_box("\n".join(linhas), altura=5)

    def gerar(self):
        self.pdf.add_page()
        self.header()
        self.add_dados_funcionario()
        self.add_exames_realizados(self.funcionario.exames_selecionados)
        self.add_sinais_vitais()
        self.add_ficha_clinica_funcionario()
        self.add_ficha_clinica_medico()
        self.add_conclusao()

class EcaminhamentoExameGerador:
    def __init__(self, pdf: FPDF, funcionario, empresa: Empresa, tipo_exame: str):
        self.pdf = pdf
        self.funcionario = funcionario
        self.empresa = empresa
        self.tipo_exame = tipo_exame
        self.largura = 190

        self.pdf.add_font("Verdana", "", "fonts/verdana.ttf", uni=True)
        self.pdf.add_font("Verdana", "B", "fonts/verdanab.ttf", uni=True)
        self.pdf.add_font("Verdana", "I", "fonts/verdanai.ttf", uni=True)
        
    def header(self):
        altura = 15
        self.pdf.set_y(1)
        self.pdf.image('logo_teca.png', 10, 4, 33)
        self.pdf.set_font("Verdana", "B", 10)
        self.pdf.cell(self.largura, altura, "Pedido de Exames",1,True,"C")
        self.pdf.ln(1)
        
    # def footer(self):
    #     self.pdf.set_y(-15)
    #     self.pdf.set_font("Verdana", "I", 8)
    #     self.pdf.cell(0, 10, f"Página {self.pdf.page_no()}", 0, 0, "C")

    def add_title(self, titulo, alinhamento="C"):
        self.pdf.set_font("Verdana", "B", 9)
        self.pdf.set_fill_color(237, 237, 237)
        self.pdf.cell(self.largura, 6, titulo, 1, ln=True, fill=True, align=alinhamento)

    def multiline_box(self, texto, altura=4.5, border=True):
        self.pdf.set_font("Verdana", "", 8)
        self.pdf.multi_cell(self.largura, altura, texto, border)

    def add_dados_funcionario(self):
        self.add_title("Dados do Funcionário")
        nome = self.funcionario.nome
        cpf = self.funcionario.cpf
        cpf_formatado = re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', cpf)
        nascimento = self.funcionario.data_nascimento.strftime("%d/%m/%Y")
        idade = self.funcionario.idade
        sexo = self.funcionario.sexo
        cargo = self.funcionario.cargo.nome
        tipo_exame = self.tipo_exame
        data_ficha = datetime.today().strftime("%d/%m/%Y")

        texto = (
            f"Nome: {nome}      CPF: {cpf_formatado}      Tipo de exame: {tipo_exame} \n"
            f"Sexo: {sexo}  Idade: {idade}  Nascimento: {nascimento}\n"
            f"Cargo: {cargo}\n"
            f"Tipo de Exame: {tipo_exame}   Data Ficha: {data_ficha}\n"
            f"Empresa: {self.empresa.razao_social}\n"
            f"CNPJ: {self.empresa.cnpj}\n"
            f"Unidade: {self.empresa.razao_social}\n"
        )
        self.multiline_box(texto)

    def add_tabela_informacoes_atendimento(self):
        self.add_title("Informações de Atendimento do Prestador")
        self.pdf.set_font("Verdana", "B", 8)
        self.pdf.cell(self.largura / 3, 4, "Tipo de atendimento", 1, 0)
        self.pdf.cell(self.largura / 3, 4, "Faixa de horário de atendimento", 1, 0)
        self.pdf.cell(self.largura / 3, 4, "Comentários", 1, 0)
        self.pdf.ln()

    def add_informacoes_atendimento(self):
        self.pdf.set_font("Verdana", "", 8)
        self.pdf.cell(self.largura / 3, 4, 'Hora Marcada', 1)
        self.pdf.cell(self.largura / 3, 4, '07:00 até 17:00', 1)
        self.pdf.cell(self.largura / 3, 4, '', 1)
        self.pdf.ln(10)

    def add_tabela_de_exames(self):
        self.add_title('Avaliação Clínica e Exames Realizados', 'L')
        cabecalho = [
            ("DATA", 0.25),
            ("EXAME", 0.25),
            ("DATA", 0.25),
            ("EXAME", 0.25),
        ]
        self.pdf.set_font("Verdana", "B", 8)
        for nome_coluna, proporcao in cabecalho:
            largura_coluna = self.largura * proporcao
            self.pdf.cell(largura_coluna, 6, nome_coluna, 1, 0, "C")
        self.pdf.ln()

    def add_exam_section(self):
        altura = 5
        self.add_tabela_de_exames()
        self.pdf.set_font("Verdana", "", 8)

        exames = self.funcionario.exames_selecionados
        largura_coluna = self.largura * 0.25

        def render_exame(exame):
            data = exame.get("data_realizacao")
            data_str = data.strftime("%d/%m/%Y") if data else ""
            nome = exame["exame"].nome
            self.pdf.cell(largura_coluna, altura, data_str, 1, align='C')
            self.pdf.cell(largura_coluna, altura, nome, 1, align='C')

        i = 0
        while i < len(exames):
            render_exame(exames[i])
            if i + 1 < len(exames):
                render_exame(exames[i + 1])
            else:
                self.pdf.cell(largura_coluna, altura, "", 1, align='C')
                self.pdf.cell(largura_coluna, altura, "", 1, align='C')
            self.pdf.ln()
            i += 2

        self.pdf.ln(15)

    def add_final_section(self):
        colaborador_nome = self.funcionario.nome
        medico_info = [
            "___________________________",
            "        Médico / CRM",
            "      ____/____/________",
        ]
        colaborador_info = [
            "___________________________",
            f"{colaborador_nome}",
            "     ____/____/________",
        ]
        altura = 5
        for i in range(0, len(medico_info)):
            y = self.pdf.get_y()
            x = self.pdf.get_x() + self.largura / 2
            self.pdf.multi_cell(self.largura / 2, altura, medico_info[i], False, align='L')
            self.pdf.set_xy(x, y)
            self.pdf.multi_cell(self.largura / 2, altura, colaborador_info[i], False, align='L')

    def gerar(self):
        self.pdf.add_page()
        self.header()
        self.add_dados_funcionario()
        self.add_tabela_informacoes_atendimento()
        self.add_informacoes_atendimento()
        self.add_exam_section()
        self.add_final_section()
