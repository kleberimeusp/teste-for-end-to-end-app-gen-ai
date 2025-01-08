from fastapi import FastAPI
from abc import ABC, abstractmethod

class RouterInitializer(ABC):
    """
    Abstract interface for initializing routers in the FastAPI application.
    """

    @abstractmethod
    def initialize(self, app: FastAPI):
        """
        Attach routers to the FastAPI application.

        Args:
            app (FastAPI): The FastAPI application instance.
        """
        pass
