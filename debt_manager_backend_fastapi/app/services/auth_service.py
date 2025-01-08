from app.models.auth import UserResponse
from app.repositories.user_repository import UserRepository
from app.models.user import User, UserCreate

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate_user(self, email: str, password: str) -> UserResponse:
        user = self.user_repository.find_by_email(email)
        if user and user.verify_password(password):
            return UserResponse(username=user.username, email=user.email)
        return None
    
    def register_user(self, user: UserCreate) -> UserResponse:
        user = self.user_repository.find_by_email(user.email)
        if user and user.verify_token(user.hashed_password):
            return self.user_repository.create(user)
        return None    
