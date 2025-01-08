from abc import abstractmethod
from app.models.user import User
from typing import Dict, Optional, Union
from .shareds.repository_interface import RepositoryInterface

class UserRepositoryInterface(RepositoryInterface[User]):
    @abstractmethod
    def find_by_email(self, email: str) -> Union[User, str]:
        """Encontra um usuário pelo email."""
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        """Encontra um usuário pelo nome de usuário."""
        pass

    @abstractmethod
    def add_user(self, user: User):
        """Adiciona um novo usuário ao repositório."""
        pass

    @abstractmethod
    def get_verify_password(self, password: str) -> Union[User, str]:
        """Encontra um usuário pela senha de usuário."""
        pass