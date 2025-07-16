from datetime import datetime, date
from cargos import Cargo
from empresas import Empresa
import streamlit as st
from kit_gerador import KitGerador
import os

class Funcionario:
    def __init__(self, nome:str, cpf:str, data_nascimento:date, data_admissao:date, cargo:Cargo, empresa:Empresa) -> None:
        self.nome = nome.strip()
        self.cpf = cpf.strip()
        self.data_nascimento = data_nascimento
        self.data_admissao = data_admissao
        self.cargo = cargo
        self.empresa = empresa
        
    def gerar_kit(self) -> str:
        gerador_de_kit = KitGerador(empresa_info=self.empresa, cargo_info=self.cargo)
        
        gerador_de_kit.create_pdf(self)

        nome_arquivo = f"aso_{self.nome.replace(' ', '_')}_{self.cpf[-4:]}.pdf"

        os.rename("aso.pdf", nome_arquivo)
        
        return nome_arquivo