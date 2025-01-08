from fastapi import FastAPI, APIRouter, HTTPException
from app.interfaces.router_initializer import RouterInitializer
from app.services.debt_service import DebtService
from typing import List, Dict

class DebtRouter(RouterInitializer):
    """
    Initializes debt-related routes for the application.
    """

    def __init__(self, debt_service: DebtService):
        """
        Initialize the DebtRouter with the DebtService dependency.

        Args:
            debt_service (DebtService): The service layer for debt operations.
        """
        self.debt_service = debt_service

    def initialize(self, app: FastAPI):
        """
        Attach debt-related routes to the FastAPI application.

        Args:
            app (FastAPI): The FastAPI application instance.
        """
        router = APIRouter()

        @router.get("/", response_model=List[Dict])
        async def get_debts():
            """
            Retrieve a list of all debts.
            """
            try:
                debts = self.debt_service.list_debts()
                return debts
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @router.get("/{debt_id}", response_model=Dict)
        async def get_debt(debt_id: str):
            """
            Retrieve a specific debt by ID.
            """
            try:
                debt = self.debt_service.get_debt_by_id(debt_id)
                return debt
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))

        @router.post("/", response_model=Dict)
        async def create_debt(debt: dict):
            """
            Create a new debt.
            """
            try:
                new_debt = self.debt_service.add_debt(debt)
                return new_debt
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @router.put("/{debt_id}", response_model=Dict)
        async def update_debt(debt_id: str, debt: dict):
            """
            Update an existing debt by ID.
            """
            try:
                updated_debt = self.debt_service.update_debt(debt_id, debt)
                return updated_debt
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @router.delete("/{debt_id}", response_model=Dict)
        async def delete_debt(debt_id: str):
            """
            Delete a debt by ID.
            """
            try:
                self.debt_service.delete_debt(debt_id)
                return {"message": f"Debt with ID {debt_id} deleted successfully."}
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        # Attach the router to the application
        app.include_router(router, prefix="/debts", tags=["Debts"])
