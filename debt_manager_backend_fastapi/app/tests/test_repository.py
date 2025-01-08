from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.config.database import SessionLocal

from sqlalchemy.orm import Session
from app.models.user import User

def test_find_by_email():
    session = SessionLocal()
    repo = UserRepository(session_factory=lambda: session)

    # Adicionar um usuário de exemplo
    user = User(username="johndoe", email="john@example.com", hashed_password="hashed_pw", name="John Doe")
    session.add(user)
    session.commit()

    # Testar o método
    found_user = repo.find_by_email("john@example.com")
    assert found_user.email == "john@example.com"

    # Testar usuário inexistente
    not_found_user = repo.find_by_email("notfound@example.com")
    assert not_found_user == "Not available"

    session.close()
