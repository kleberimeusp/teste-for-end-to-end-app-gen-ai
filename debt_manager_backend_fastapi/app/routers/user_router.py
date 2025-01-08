from fastapi import FastAPI, APIRouter, HTTPException
from app.interfaces.router_initializer import RouterInitializer
from app.services.user_service import UserService
from typing import List, Dict

class UserRouter(RouterInitializer):
    """
    Initializes user-related routes for the application.
    """

    def __init__(self, user_service: UserService):
        """
        Initialize the router with a service dependency.

        Args:
            user_service (UserService): The service layer for user logic.
        """
        self.user_service = user_service

    def initialize(self, app: FastAPI):
        """
        Attach user-related routes to the FastAPI application.

        Args:
            app (FastAPI): The FastAPI application instance.
        """
        router = APIRouter()

        @router.get("/", response_model=List[Dict])
        async def get_users():
            """
            Retrieve a list of users.
            """
            try:
                users = self.user_service.get_users()
                return users
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @router.get("/{user_id}", response_model=Dict)
        async def get_user(user_id: str):
            """
            Retrieve a specific user by ID.
            """
            try:
                user = self.user_service.get_user_by_id(user_id)
                return user
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))

        @router.post("/", response_model=Dict)
        async def create_user(user: dict):
            """
            Create a new user.
            """
            try:
                new_user = self.user_service.create_user(user)
                return new_user
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @router.put("/{user_id}", response_model=Dict)
        async def update_user(user_id: str, user: dict):
            """
            Update an existing user by ID.
            """
            try:
                updated_user = self.user_service.update_user(user_id, user)
                return updated_user
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @router.delete("/{user_id}", response_model=Dict)
        async def delete_user(user_id: str):
            """
            Delete a user by ID.
            """
            try:
                deleted_user = self.user_service.delete_user(user_id)
                return {"message": f"User with ID {user_id} deleted successfully."}
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        # Attach the router to the application
        app.include_router(router, prefix="/users", tags=["Users"])
