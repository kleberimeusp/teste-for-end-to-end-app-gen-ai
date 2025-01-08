from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.debt import DebtRequest, DebtResponse
from app.services.debt_service import DebtService

class DebtController:
    def __init__(self, debt_service: DebtService):
        self.debt_service = debt_service
        self.router = APIRouter()
        self.router.add_api_route("/", self.get_all_debts, methods=["GET"], response_model=List[DebtResponse])
        self.router.add_api_route("/", self.create_debt, methods=["POST"], response_model=DebtResponse)
        self.router.add_api_route("/{debt_id}", self.get_debt, methods=["GET"], response_model=DebtResponse)
        self.router.add_api_route("/{debt_id}", self.delete_debt, methods=["DELETE"])
        self.router.add_api_route("/paginate", self.paginate_debts, methods=["GET"], response_model=List[DebtResponse])

    async def get_all_debts(self, skip: int = 0, limit: int = 10):
        """
        Get all debts with pagination and return a list of DebtResponse objects.
        """
        try:
            debt_responses = self.debt_service.get_all_debts(skip, limit)
            return debt_responses
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

    async def create_debt(self, debt: DebtRequest) -> DebtResponse:
        """
        Create a new debt.
        """
        try:
            return self.debt_service.create_debt(debt)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_debt(self, debt_id: str):
        """
        Get a debt by ID.
        """
        try:
            return self.debt_service.get_debt_by_id(debt_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def delete_debt(self, debt_id: str):
        """
        Delete a debt by ID.
        """
        try:
            self.debt_service.delete_debt(debt_id)
            return {"message": f"Debt {debt_id} deleted successfully."}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def paginate_debts(self, page: int = 1, page_size: int = 10):
        """
        Paginate debts with metadata.
        """
        try:
            debts = self.debt_service.paginate_debts(page, page_size)
            return debts
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
