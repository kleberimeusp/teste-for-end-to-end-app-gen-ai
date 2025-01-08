from fastapi import FastAPI
from typing import List
from app.interfaces.router_initializer import RouterInitializer

class AppSetup:
    """
    Manages the setup and initialization of the FastAPI application.
    """

    def __init__(self, app: FastAPI, router_initializers: List[RouterInitializer]):
        self.app = app
        self.router_initializers = router_initializers

    def setup_routers(self):
        for router_initializer in self.router_initializers:
            router_initializer.initialize(self.app)
