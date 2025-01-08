from typing import Dict
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from app.interfaces.router_initializer import RouterInitializer
from app.models.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm

class AuthRouter(RouterInitializer):
    """
    Initializes authentication-related routes for the application.
    """

    def __init__(self, auth_service: AuthService):
        """
        Initialize the AuthRouter with the AuthService dependency.

        Args:
            auth_service (AuthService): The service layer for authentication.
        """
        self.auth_service = auth_service

    def initialize(self, app: FastAPI):
        """
        Attach authentication-related routes to the FastAPI application.

        Args:
            app (FastAPI): The FastAPI application instance.
        """
        router = APIRouter()

        @router.post("/login")
        async def login(form_data: OAuth2PasswordRequestForm = Depends()):
            """
            Authenticate a user and return a JWT token.

            Args:
                form_data (OAuth2PasswordRequestForm): Form data containing username and password.

            Returns:
                dict: A dictionary containing the access token and its type.
            """
            try:
                token = self.auth_service.authenticate_user(form_data.username, form_data.password)
                return {"access_token": token, "token_type": "bearer"}
            except ValueError as e:
                raise HTTPException(status_code=401, detail=str(e))


        @router.post("/register", response_model=Dict)
        async def register(user: dict):
            """
            Register a new user.

            Args:
                user (UserCreate): User details for registration.

            Returns:
                UserResponse: The registered user's details.
            """
            try:
                new_user = UserCreate(**user)
                response = self.auth_service.register_user(new_user)
                return response
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        app.include_router(router, prefix="/auth", tags=["Auth"])