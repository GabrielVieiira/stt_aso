from datetime import datetime, date
from cargos import Cargo
from empresas import Empresa
from kit_gerador import AsoGerador, FichaClinicaGerador, EcaminhamentoExameGerador
import zipfile
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
        gerador_de_aso = AsoGerador(self, empresa_info=self.empresa, tipo_de_exame=tipo_de_exame)
        gerador_de_ficha_clinica = FichaClinicaGerador(self, self.empresa, tipo_de_exame, self.cargo)
        gerador_de_encaminhamento_de_exame = EcaminhamentoExameGerador(self, self.empresa, tipo_de_exame)
        
        buffer_aso = BytesIO()
        buffer_ficha = BytesIO()
        buffer_encaminhamento = BytesIO()

        aso_pdf_str = gerador_de_aso.create_pdf()
        buffer_aso.write(aso_pdf_str.encode('latin-1'))

        ficha_pdf_str = gerador_de_ficha_clinica.create_pdf()
        buffer_ficha.write(ficha_pdf_str.encode('latin-1'))

        encaminhamento_pdf_str = gerador_de_encaminhamento_de_exame.create_pdf()
        buffer_encaminhamento.write(encaminhamento_pdf_str.encode('latin-1'))

        buffer_aso.seek(0)
        buffer_ficha.seek(0)
        buffer_encaminhamento.seek(0)
        
        nome_formatado = self.nome.replace(" ", "_")

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr(f"ASO_{nome_formatado}.pdf", aso_pdf_str.encode("latin-1"))
            zipf.writestr(f"Ficha_Clinica_{nome_formatado}.pdf", ficha_pdf_str.encode("latin-1"))
            zipf.writestr(f"Encaminhamento_Exame_{nome_formatado}.pdf", encaminhamento_pdf_str.encode("latin-1"))

        zip_buffer.seek(0)
        return zip_buffer

    def _calcular_idade(self) -> int:
        hoje = datetime.today().date()
        idade = hoje.year - self.data_nascimento.year
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1
        return idade
