from asyncpg import CaseNotFoundError
from fastapi import HTTPException
from sqlalchemy import text
from app.middlewares.jwt_middleware import decode_jwt, generate_jwt
from app.models.user import User, UserCreate
from typing import Dict, List, Optional, Union
from app.models.user import User

from app.models.user import User
from app.repositories.generic_repository import GenericRepository
from app.repositories.interfaces.user_repository_interface import UserRepositoryInterface
from typing import Optional

from app.config.database import SessionLocal

class CaseNotFoundError(HTTPException):
    """Exceção para indicar que um caso foi encontrado."""
    def __init__(self, detail: str = "Item encontrado, não pode inserir", data: str = ""):
        super().__init__(status_code=204, detail=detail)
        super().__init__(status_code=200, detail=detail, data=data)
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message       

class UserRepository(GenericRepository[User], UserRepositoryInterface):
    def __init__(self):
        super().__init__(session_factory=SessionLocal, model=User)

        # Inicializa o atributo users como uma lista vazia
        self.users = []

        self.session_factory = SessionLocal

        # Adiciona usuários com os campos corretos
        self.add_user(User(
            id=1,
            email="user@example.com",
            username="testuser",
            hashed_password="hashedpassword123",  # Substitua por um hash real
            name="Test User"
        ))


    def find_by_id (self, id: str) -> Union[User, str]:
        return super().get_by_id(id=id)
              

    def get_verify_password(self, password: str) -> Union[User, str]:
        with self.session_factory() as session:
            # Parametrized query to avoid SQL Injection
            result = session.execute(
                text('SELECT * FROM "Users" WHERE hashed_password = :password'),
                {"hashed_password": decode_jwt(password)}
            )

            # Fetch the first result
            row = result.fetchone()

            if row:
                # If a user is found, raise CaseNotFoundError
                raise CaseNotFoundError(f"User with password '{password}' already exists.")
        
        return False
    
    def get_verify_token(self, hashed_password: str) -> Union[User, str]:
        password = decode_jwt(hashed_password)
        if password is None:
            return False
        else:
            return True


    def find_by_email(self, email: str) -> Union[User, str]:
      with self.session_factory() as session:
        # Parametrized query to avoid SQL Injection
        result = session.execute(
            text('SELECT * FROM Users WHERE email = :email'),
            {"email": email}
        )

        # Fetch the first result
        row = result.fetchone()

        if row:
            # If a user is found, raise CaseNotFoundError
            raise CaseNotFoundError(f"User with email '{email}' already exists.")
        
        return False

    def add_user(self, user: User):
        self.users.append(user)

    def save(self, user: User):
        return super().save(user, "public.users_users_uuid_seq", user)

    def find_all(self, page: int = 1, per_page: int = 10) -> dict:
        return super().find_all(page=page, per_page=per_page)

    def find_by_username(self, username: str) -> Optional[User]:
        return next((user for user in self.users if user.username == username), None)

    def create(self, data: UserCreate) -> Optional[User]:
        try:

            user = User(**{key: value for key, value in data.dict().items() if key != "password"})
            user.hashed_password = generate_jwt(data.password)
            
            # Save the new User to the database
            user.id = super().save(user, sequence_name="public.users_users_uuid_seq", entity_class=User)

            return user
        except Exception as e:
            # Log the exception if logging is available, or handle the error as needed
            print(f"Error creating user: {e}")
            return None