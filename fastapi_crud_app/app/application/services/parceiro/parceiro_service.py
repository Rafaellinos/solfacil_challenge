from typing import List, Optional
from fastapi_crud_app.app.application.ports.parceiro.parceiro_repository import AbstractParceiroRepository
from fastapi_crud_app.app.domain.models.parceiro.parceiro import Parceiro
from fastapi_crud_app.app.domain.usecases.parceiro.import_csv import AbstractImportCSV


class ParceiroService:
    def __init__(
            self,
            repo: AbstractParceiroRepository,
            usecase: AbstractImportCSV,
    ):
        self.repo = repo
        self.usecase = usecase

    def upload(self, file: str):
        ...

    def get_all_parceiros(self) -> List[Parceiro]:
        return self.repo.get_all()

    def get_parceiro_by_id(self, id: int) -> Optional[Parceiro]:
        return self.repo.get_by_id(id)

    def create_parceiro(self, parceiro: Parceiro) -> Parceiro:
        return self.repo.add(parceiro)

    def update_parceiro(self, parceiro: Parceiro) -> Parceiro:
        return self.repo.update(parceiro)

    def delete_parceiro(self, id: int) -> None:
        self.repo.delete(id)
