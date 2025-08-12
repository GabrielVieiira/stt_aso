from datetime import datetime, date
from cargos import Cargo
from empresas import Empresa
from kit_gerador import AsoGerador, FichaClinicaGerador, EcaminhamentoExameGerador
from fpdf import FPDF
from io import BytesIO

class Funcionario:
    def __init__(
        self,
        nome:str,
        cpf:str,
        data_nascimento:date,
        # data_admissao:date,
        cargo:Cargo,
        empresa:Empresa,
        sexo:str,
        exames_selecionados:list[dict]
        ) -> None:
        self.nome = nome.strip()
        self.cpf = cpf.strip()
        self.data_nascimento = data_nascimento
        # self.data_admissao = data_admissao
        self.cargo = cargo
        self.empresa = empresa
        self.idade = self._calcular_idade()
        self.sexo = sexo
        self.exames_selecionados = exames_selecionados
    
    def gerar_kit(self, tipo_de_exame: str) -> BytesIO:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Geração das páginas diretamente no mesmo PDF
        AsoGerador(pdf, self, self.empresa, tipo_de_exame).gerar()
        FichaClinicaGerador(pdf, self, self.empresa, tipo_de_exame, self.cargo).gerar()
        EcaminhamentoExameGerador(pdf, self, self.empresa, tipo_de_exame).gerar()

        # Geração do PDF em memória
        pdf_buffer = BytesIO()
        pdf_output = pdf.output(dest='S').encode('latin1') 
        pdf_buffer.write(pdf_output)
        pdf_buffer.seek(0)

        return pdf_buffer

    def _calcular_idade(self) -> int:
        hoje = datetime.today().date()
        idade = hoje.year - self.data_nascimento.year
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1
        return idade
