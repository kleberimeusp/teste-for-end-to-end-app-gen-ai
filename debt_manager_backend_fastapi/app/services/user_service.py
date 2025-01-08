from fastapi import HTTPException, status
from flask import jsonify
from app.repositories.user_repository import UserRepository
from app.models.user import UserCreate, UserResponse

from app.repositories.user_repository import UserRepository
from app.models.user import UserCreate, UserResponse, UserUpdate
from typing import Dict, List



class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository


    def create_user(self, data: UserCreate) -> UserResponse:
 
        if self.user_repository.find_by_email(data.email) == True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": f"User with email '{data.email}' already exists."}
            )

        new_user = self.user_repository.create(data)
        response = UserResponse(**new_user.to_dict())
        return response


    def get_user_by_id(self, user_id: str) -> UserResponse:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "User not found."}
            )               
        return UserResponse(**user.dict())

    def update_user(self, user_id: str, data: UserUpdate) -> UserResponse:
        existing_user = self.user_repository.find_by_id(user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "User not found."}
            )  
        updated_user = self.user_repository.update(user_id, data)
        return UserResponse(**updated_user.dict())

    def delete_user(self, user_id: str) -> None:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "User not found."}
            ) 
        self.user_repository.delete(user_id)

    def get_all_users(self, skip: int = 0, limit: int = 10) -> dict:
        users = self.user_repository.find_all(skip, limit)
        if not users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "User not found."}
            ) 
        records = users['data']['records']
        response: List[UserResponse] = []
        for user in records:
            response.append(UserResponse(**user))
        return response

    def paginate_users(self, page: int, page_size: int) -> Dict:
        total_users = self.user_repository.count()
        users = self.user_repository.find_all(
            skip=(page - 1) * page_size, limit=page_size
        )
        return {
            "total": total_users,
            "page": page,
            "page_size": page_size,
            "users": [UserResponse(**user.dict()) for user in users],
        }
