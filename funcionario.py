from datetime import datetime, date
from cargos import Cargo
from empresas import Empresa
import streamlit as st
from kit_gerador import AsoGerador, FichaClinicaGerador
import os

class Funcionario:
    def __init__(self, nome:str, cpf:str, data_nascimento:date, data_admissao:date, cargo:Cargo, empresa:Empresa, sexo:str) -> None:
        self.nome = nome.strip()
        self.cpf = cpf.strip()
        self.data_nascimento = data_nascimento
        self.data_admissao = data_admissao
        self.cargo = cargo
        self.empresa = empresa
        self.idade = self._calcular_idade()
        self.sexo = sexo

    def gerar_kit(self, tipo_de_exame:str) -> str:
        gerador_de_aso = AsoGerador(empresa_info=self.empresa, cargo_info=self.cargo)
        gerador_de_ficha_clinica = FichaClinicaGerador(self, self.empresa,tipo_de_exame, self.cargo)


        nome_arquivo_aso = f"aso_{self.nome.replace(' ', '_')}_{self.cpf[-4:]}.pdf"
        nome_arquivo_ficha_clinica = f"ficha_clinica_{self.nome.replace(' ', '_')}_{self.cpf[-4:]}.pdf"

        gerador_de_aso.create_pdf(self, tipo_de_exame, nome_arquivo_aso)
        gerador_de_ficha_clinica.create_pdf(nome_arquivo_ficha_clinica)


        return nome_arquivo_ficha_clinica, nome_arquivo_aso

    def _calcular_idade(self) -> int:
        """Calcula a idade do funcionário baseado na data de nascimento"""
        hoje = datetime.today().date()  # Obtém a data de hoje
        idade = hoje.year - self.data_nascimento.year  # Subtrai o ano
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):  # Verifica se já fez aniversário este ano
            idade -= 1
        return idade
