from abc import ABC, abstractmethod
from typing import List, Optional
from fastapi_crud_app.app.domain.models.parceiro import Parceiro

class AbstractParceiroRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Parceiro]:
        pass

    @abstractmethod
    def get_by_id(self, parceiro_id: int) -> Optional[Parceiro]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Parceiro]:
        pass

    @abstractmethod
    def add(self, parceiro: Parceiro) -> Parceiro:
        pass

    @abstractmethod
    def delete(self, parceiro_id: int) -> None:
        pass

    @abstractmethod
    def update(self, parceiro: Parceiro) -> Parceiro:
        pass
