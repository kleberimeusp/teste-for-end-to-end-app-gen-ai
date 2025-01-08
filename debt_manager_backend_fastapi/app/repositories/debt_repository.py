from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, Union
from app.config.database import SessionLocal
from app.models.debt import Debt, DebtCreate
from app.repositories.generic_repository import GenericRepository
from app.repositories.interfaces.debt_repository_interface import DebtRepositoryInterface

class CaseNotFoundError(HTTPException):
    """Exceção para indicar que um caso foi encontrado."""
    def __init__(self, detail: str = "Item encontrado, não pode inserir", data: str = ""):
        super().__init__(status_code=204, detail=detail)
        super().__init__(status_code=200, detail=detail, data=data)
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message     
        
class DebtRepository(GenericRepository[Debt], DebtRepositoryInterface):

    def __init__(self, detail: str = "Item encontrado, não pode inserir", data: str = ""):
        super().__init__(session_factory=SessionLocal, model=Debt)
        self.session_factory = SessionLocal
 

    def get_by_id(self, debt_id: str) -> Union[Debt, str]:
        """
        Retrieve a debt by ID.
        """
        return super().get_by_id(id=debt_id)

    def find_by_description(self, description: str) -> Optional[Debt]:
        """
        Find a debt by its description.
        """
        with self.session_factory() as session:
            result = session.execute(
                text('SELECT * FROM "Debts" WHERE description = :description'),
                {"description": description}
            )
            row = result.fetchone()
            return Debt(**row) if row else None

    def create(self, data: DebtCreate) -> Optional[Debt]:
        """
        Create a new debt record.
        """
        try:
            debt = Debt(**data.dict())
            debt.id = super().save(debt, sequence_name="public.debts_debts_uuid_seq", entity_class=Debt)
            return debt
        except SQLAlchemyError as e:
            print(f"Error creating debt: {e}")
            return None

    def save(self, debt: Debt):
        """
        Save a debt to the database.
        """
        return super().save(debt, "public.debts_debts_uuid_seq", debt)

    def find_all(self, page: int = 1, per_page: int = 10) -> dict:
        """
        Retrieve all debts with pagination.
        """
        return super().find_all(page=page, per_page=per_page)

    def delete(self, debt_id: str) -> None:
        """
        Delete a debt by ID.
        """
        try:
            with self.session_factory() as session:
                session.execute(
                    text('DELETE FROM "Debts" WHERE id = :id'),
                    {"id": debt_id}
                )
                session.commit()
        except SQLAlchemyError as e:
            print(f"Error deleting debt: {e}")
            raise e
        
    def add_debt(self, debt: Debt):
        self.users.append(debt)