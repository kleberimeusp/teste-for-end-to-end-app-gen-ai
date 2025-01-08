from fastapi import FastAPI
from app.repositories.debt_repository import DebtRepository
from app.routers.auth_router import AuthRouter
from app.routers.debt_router import DebtRouter
from app.routers.user_router import UserRouter
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.services.debt_service import DebtService
from app.services.user_service import UserService

# FastAPI App Initialization
app = FastAPI(
    title="Debt Manager API",
    description=(
        "This API allows users to manage their debts efficiently. "
        "It provides endpoints for user authentication, debt tracking, and overall debt management."
    ),
    version="1.0.0",
)

# Dependency Injection for User
user_repository = UserRepository()
user_service = UserService(user_repository)
user_router = UserRouter(user_service)

# Dependency Injection for Auth
auth_service = AuthService(user_repository)  # Auth depends on UserRepository
auth_router = AuthRouter(auth_service)

# Dependency Injection for Debt
debt_repository = DebtRepository()
debt_service = DebtService(debt_repository)
debt_router = DebtRouter(debt_service)

# Initialize Routers
user_router.initialize(app)
auth_router.initialize(app)
debt_router.initialize(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
