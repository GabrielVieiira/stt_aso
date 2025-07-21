from datetime import datetime, date
from cargos import Cargo
from empresas import Empresa
from kit_gerador import AsoGerador, FichaClinicaGerador, EcaminhamentoExameGerador

class Funcionario:
    def __init__(
        self,
        nome:str,
        cpf:str,
        data_nascimento:date,
        data_admissao:date,
        cargo:Cargo,
        empresa:Empresa,
        sexo:str,
        exames_selecionados:list[dict]
        ) -> None:
        self.nome = nome.strip()
        self.cpf = cpf.strip()
        self.data_nascimento = data_nascimento
        self.data_admissao = data_admissao
        self.cargo = cargo
        self.empresa = empresa
        self.idade = self._calcular_idade()
        self.sexo = sexo
        self.exames_selecionados = exames_selecionados

    def gerar_kit(self, tipo_de_exame:str) -> str:
        gerador_de_aso = AsoGerador(self, empresa_info=self.empresa, tipo_de_exame=tipo_de_exame)
        gerador_de_ficha_clinica = FichaClinicaGerador(self, self.empresa, tipo_de_exame, self.cargo)
        gerador_de_encaminhamento_de_exame = EcaminhamentoExameGerador(self, self.empresa, tipo_de_exame)


        nome_arquivo_aso = f"aso_{self.nome.replace(' ', '_')}_{self.cpf[-4:]}.pdf"
        nome_arquivo_ficha_clinica = f"ficha_clinica_{self.nome.replace(' ', '_')}_{self.cpf[-4:]}.pdf"
        nome_arquivo_encaminhamento_exame = f"encaminhamento_de_exame_{self.nome.replace(' ', '_')}_{self.cpf[-4:]}.pdf"

        gerador_de_aso.create_pdf(nome_arquivo_aso)
        gerador_de_ficha_clinica.create_pdf(nome_arquivo_ficha_clinica)
        gerador_de_encaminhamento_de_exame.create_pdf(nome_arquivo_encaminhamento_exame)


        return nome_arquivo_ficha_clinica, nome_arquivo_aso, nome_arquivo_encaminhamento_exame

    def _calcular_idade(self) -> int:
        hoje = datetime.today().date()
        idade = hoje.year - self.data_nascimento.year
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1
        return idade
