from io import StringIO
from typing import List, Dict
import re

import pandas as pd

from app.application.dtos.parceiro_dto import ParceiroDto
from app.application.ports.parceiro.parceiro_repository import AbstractParceiroRepository
from app.application.usecases.parceiro.abstract_import_csv import AbstractImportCsvUseCase
from app.domain.entities.parceiro.parceiro import Parceiro


class ImportCsvUseCase(AbstractImportCsvUseCase):
    def __init__(self, parceiro_repository: AbstractParceiroRepository):
        self.parceiro_repository = parceiro_repository

    def __sanitize_string(self, string: str) -> str:
        # remove special characters using regex
        if not string:
            return ""
        return re.sub(r"[^a-zA-Z0-9]+", "", string)

    def __commit_parceiro(self, parceiro: Parceiro) -> ParceiroDto:
        if parceiro.id:
            return self.parceiro_repository.update(parceiro)
        return self.parceiro_repository.add(parceiro)

    def execute(self, csv_content: str) -> Dict[str, List[ParceiroDto]]:
        df = pd.read_csv(StringIO(csv_content))

        parceiros_to_process = []
        for _, row in df.iterrows():
            parceiro = Parceiro(
                cnpj=self.__sanitize_string(row.get('CNPJ')),
                razao_social=row.get('Razão Social'),
                nome_fantasia=row.get('Nome Fantasia'),
                telefone=self.__sanitize_string(row.get('Telefone')),
                email=row.get('Email'),
                cep=self.__sanitize_string(row.get('CEP')),
            )
            existing_parceiro = self.parceiro_repository.get_by_cnpj(parceiro.cnpj)
            if existing_parceiro:
                parceiro.id = existing_parceiro.id
            parceiros_to_process.append(parceiro)

        parceiros = {"created": [], "updated": []}
        for parceiro in parceiros_to_process:
            if parceiro.id:
                parceiros["updated"].append(
                    self.parceiro_repository.update(parceiro)
                )
            else:
                parceiros["created"].append(
                    self.parceiro_repository.add(parceiro)
                )
        return parceiros
