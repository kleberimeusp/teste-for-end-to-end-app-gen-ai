from abc import ABC, abstractmethod
from typing import Dict, Generic, TypeVar

T = TypeVar('T')  # Tipo genérico

class RepositoryInterface(ABC, Generic[T]):
    @abstractmethod
    def find_all(self, page: int = 1, per_page: int = 10) -> dict:
        """Recupera todos os itens com paginação."""
        pass

    @abstractmethod
    def save(self, entity: T):
        """Salva a entidade no repositório."""
        pass

    @abstractmethod
    def create(self, data: T) -> T:
        """Cria uma nova entidade."""
        pass

    def get_by_id(self, id: T) -> T:
        """Recupera uma unico registro."""
        pass