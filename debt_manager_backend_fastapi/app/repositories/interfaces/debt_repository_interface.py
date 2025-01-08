from abc import abstractmethod
from app.models.debt import Debt
from typing import Dict
from .shareds.repository_interface import RepositoryInterface

class DebtRepositoryInterface(RepositoryInterface[Debt]):
    @abstractmethod
    def add_debt(self, debt: Debt):
        """Adiciona uma nova dívida ao repositório."""
        pass
