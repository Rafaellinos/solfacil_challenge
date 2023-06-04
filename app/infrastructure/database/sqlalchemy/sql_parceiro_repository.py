from typing import Optional

from app.application.dtos.parceiro_dto import ParceiroDto
from app.application.ports.parceiro.parceiro_repository import AbstractParceiroRepository
from app.domain.entities.parceiro.parceiro import Parceiro
from app.infrastructure.database.sqlalchemy.models import ParceiroModel
from app.infrastructure.database.sqlalchemy.session import get_db, SessionLocal


class SqlAlchemyParceiroRepository(AbstractParceiroRepository):

    def __init__(self):
        self.session: SessionLocal = get_db()

    def add(self, parceiro: Parceiro) -> ParceiroDto:
        db_parceiro = ParceiroModel(**parceiro.dict())
        with self.session as session:
            session.add(db_parceiro)
            session.commit()
            session.refresh(db_parceiro)
        return ParceiroDto(**db_parceiro.__dict__)

    def get_by_cnpj(self, cnpj: str) -> Optional[ParceiroDto]:
        with self.session as session:
            db_parceiro = session.query(
                ParceiroModel
            ).filter(
                ParceiroModel.cnpj == cnpj
            ).first()
        return ParceiroDto(**db_parceiro.__dict__) if db_parceiro else None

    def update(self, parceiro: Parceiro) -> ParceiroDto:
        with self.session as session:
            db_parceiro = session.query(
                ParceiroModel
            ).filter(
                ParceiroModel.id == parceiro.id
            ).first()
        if db_parceiro:
            for key, value in parceiro.dict().items():
                setattr(db_parceiro, key, value)
            self.session.commit()
            self.session.refresh(db_parceiro)
        return ParceiroDto(**db_parceiro.__dict__)

    def get_all(self) -> list[ParceiroDto]:
        with self.session as session:
            db_parceiros = session.query(ParceiroModel).all()
        return [ParceiroDto(**db_parceiro.__dict__) for db_parceiro in db_parceiros]

    def delete(self, parceiro_id: int) -> None:
        with self.session as session:
            if db_parceiro := session.query(ParceiroModel).filter(
                    ParceiroModel.id == parceiro_id
            ).first():
                self.session.delete(db_parceiro)
                self.session.commit()

    def get_by_id(self, parceiro_id: int) -> Optional[ParceiroDto]:
        with self.session as session:
            db_parceiro = session.query(ParceiroModel).filter(
                ParceiroModel.id == parceiro_id
            ).first()
            return ParceiroDto(**db_parceiro.__dict__) if db_parceiro else None

    def get_by_email(self, email: str) -> Optional[ParceiroDto]:
        with self.session as session:
            if db_parceiro := session.query(ParceiroModel).filter(
                ParceiroModel.email == email
            ).first():
                return ParceiroDto(**db_parceiro.__dict__) if db_parceiro else None
