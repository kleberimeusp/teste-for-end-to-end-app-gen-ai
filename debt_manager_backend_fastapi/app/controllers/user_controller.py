from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.user import UserRequest, UserResponse
from app.services.user_service import UserService

class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.router = APIRouter()
        self.router.add_api_route("/", self.get_all_users, methods=["GET"], response_model=List[UserResponse])
        self.router.add_api_route("/", self.create_user, methods=["POST"], response_model=UserResponse)
        self.router.add_api_route("/{user_id}", self.get_user, methods=["GET"], response_model=UserResponse)
        self.router.add_api_route("/{user_id}", self.delete_user, methods=["DELETE"])

    async def get_all_users(self, skip: int = 0, limit: int = 10):
        """
        Get all users with pagination and return a list of UserResponse objects.
        """
        try:
            user_responses = self.user_service.get_all_users(skip, limit)
            return user_responses
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

    async def create_user(self, user: UserRequest) -> UserResponse:
        """
        Create a new user.
        """
        try:
            return self.user_service.create_user(user)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_user(self, user_id: str):
        """
        Get a user by ID.
        """
        try:
            return self.user_service.get_user_by_id(user_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def delete_user(self, user_id: str):
        """
        Delete a user by ID.
        """
        try:
            self.user_service.delete_user(user_id)
            return {"message": f"User {user_id} deleted successfully."}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        

    async def paginate_users(self, page: int = 1, page_size: int = 10):
        """
        Paginate users with metadata.
        """
        try:
            users = self.user_service.paginate_users(page, page_size)
            raise HTTPException(status_code=200, detail="Operação realizada com sucesso", data=users)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

   
