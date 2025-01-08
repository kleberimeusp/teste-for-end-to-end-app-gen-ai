from typing import List, Dict
from fastapi import HTTPException
from app.models.debt import DebtCreate, DebtUpdate, DebtResponse
from app.repositories.debt_repository import DebtRepository


class DebtService:
    """
    Service layer to handle debt-related business logic.
    """

    def __init__(self, debt_repository: DebtRepository):
        """
        Initialize the DebtService with a repository dependency.

        Args:
            debt_repository (DebtRepository): The repository layer for debt operations.
        """
        self.debt_repository = debt_repository

    def create_debt(self, data: DebtCreate) -> DebtResponse:
        """
        Create a new debt.

        Args:
            data (DebtCreate): Data to create the debt.

        Returns:
            DebtResponse: The created debt.
        """
        # Check if a debt with the same description already exists
        if self.debt_repository.find_by_description(data.description):
            raise HTTPException(
                status_code=400,
                detail=f"Debt with description '{data.description}' already exists."
            )
        
        # Create a new debt
        new_debt = self.debt_repository.create(data)
        return DebtResponse(**new_debt.dict())

    def get_debt_by_id(self, debt_id: str) -> DebtResponse:
        """
        Retrieve a debt by ID.

        Args:
            debt_id (str): The ID of the debt.

        Returns:
            DebtResponse: The retrieved debt.
        """
        debt = self.debt_repository.get_by_id(debt_id)
        if not debt:
            raise HTTPException(
                status_code=404,
                detail=f"Debt with ID '{debt_id}' not found."
            )
        return DebtResponse(**debt.dict())

    def update_debt(self, debt_id: str, data: DebtUpdate) -> DebtResponse:
        """
        Update an existing debt by ID.

        Args:
            debt_id (str): The ID of the debt to update.
            data (DebtUpdate): The updated debt data.

        Returns:
            DebtResponse: The updated debt.
        """
        existing_debt = self.debt_repository.get_by_id(debt_id)
        if not existing_debt:
            raise HTTPException(
                status_code=404,
                detail=f"Debt with ID '{debt_id}' not found."
            )
        
        updated_debt = self.debt_repository.update(debt_id, data)
        return DebtResponse(**updated_debt.dict())

    def delete_debt(self, debt_id: str) -> None:
        """
        Delete a debt by ID.

        Args:
            debt_id (str): The ID of the debt to delete.
        """
        debt = self.debt_repository.get_by_id(debt_id)
        if not debt:
            raise HTTPException(
                status_code=404,
                detail=f"Debt with ID '{debt_id}' not found."
            )
        
        self.debt_repository.delete(debt_id)

    def get_all_debts(self, skip: int = 0, limit: int = 10) -> List[DebtResponse]:
        """
        Retrieve all debts with pagination.

        Args:
            skip (int): Number of records to skip. Default is 0.
            limit (int): Maximum number of records to return. Default is 10.

        Returns:
            List[DebtResponse]: A list of debts.
        """
        debts = self.debt_repository.find_all(skip=skip, limit=limit)
        return [DebtResponse(**debt.dict()) for debt in debts]

    def paginate_debts(self, page: int, page_size: int) -> Dict:
        """
        Paginate debts.

        Args:
            page (int): The current page number.
            page_size (int): The number of records per page.

        Returns:
            Dict: Paginated result containing total count, page number, and debts.
        """
        total_debts = self.debt_repository.count()
        debts = self.debt_repository.find_all(
            skip=(page - 1) * page_size, limit=page_size
        )
        return {
            "total": total_debts,
            "page": page,
            "page_size": page_size,
            "debts": [DebtResponse(**debt.dict()) for debt in debts],
        }
