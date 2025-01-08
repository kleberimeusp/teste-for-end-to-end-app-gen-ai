from fastapi import FastAPI
from typing import List
from app.interfaces.router_initializer import RouterInitializer

class AppSetup:
    """
    Manages the initialization and setup of the FastAPI application.
    """

    def __init__(self, app: FastAPI, router_initializers: List[RouterInitializer]):
        """
        Initialize the application setup with the given routers.

        Args:
            app (FastAPI): The FastAPI instance.
            router_initializers (List[RouterInitializer]): A list of router initializers to configure the app.
        """
        self.app = app
        self.router_initializers = router_initializers

    def setup_routers(self):
        """
        Setup all routers in the application.
        """
        for router_initializer in self.router_initializers:
            router_initializer.initialize(self.app)
