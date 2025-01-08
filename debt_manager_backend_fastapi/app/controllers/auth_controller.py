from fastapi import APIRouter, HTTPException
from app.models.auth import UserRequest, UserResponse
from app.models.user import UserCreate
from app.services.auth_service import AuthService
from app.services.user_service import UserService

class AuthController:
    def __init__(self, 
                 auth_service: AuthService, 
                 user_service: UserService):
        self.auth_service = auth_service
        self.user_service = user_service
        self.router = APIRouter()
        self.router.add_api_route("/register", self.register, methods=["POST"], response_model=UserResponse)
        self.router.add_api_route("/login", self.login, methods=["POST"])

    async def register(self, user: UserCreate):
        """
        Register a new user.
        """
        try:
            new_user = self.auth_service.register_user(user)
            return new_user
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def login(self, user: UserRequest):
        try:
            return self.auth_service.authenticate(user.email, user.password)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
