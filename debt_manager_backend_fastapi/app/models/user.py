from pydantic import BaseModel, ConfigDict, EmailStr

from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

from uuid import UUID

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.middlewares.jwt_middleware import decode_jwt

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    hashed_password = Column(Text, nullable=False)


    def to_dict(self) -> dict:
        """
        Converte a instância do usuário para um dicionário.
        
        Returns:
            dict: Representação do usuário como dicionário.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "name": self.name,
        }
    
    def verify_password(self, password: str):
        decode_password = decode_jwt(password)
        if decode_password is None:
            return False
        else:
            return True
    
    def verify_token(self, hashed_password: str):
        decode_password = decode_jwt(hashed_password)
        if decode_password is None:
            return False
        else:
            return True    
        


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    name: str
    password: str
    
    model_config = ConfigDict(arbitrary_types_allowed=True)  # Allow arbitrary types

# Pydantic Schemas
class UserRequest(BaseModel):
    username: str
    email: EmailStr
    name: str
    password: str

class UserUpdate(BaseModel):
    id: str
    username: str
    email: EmailStr
    name: str
    hashed_password: str

    def check_password(self, password: str) -> bool:
        # Simula a verificação do hash
        return self.hashed_password == f"hashed_{password}"   


class UserResponse(BaseModel):
    id: UUID  # Change from str to UUID
    name: str
    email: EmailStr
    username: str
    hashed_password: str

    model_config = ConfigDict(arbitrary_types_allowed=True) 
    
    def to_dict(self) -> dict:
        """
        Converte a instância do usuário para um dicionário.
        
        Returns:
            dict: Representação do usuário como dicionário.
        """
        return {
            "id": str(self.id),  # Convert UUID to string for serialization
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "hashed_password": self.hashed_password,
        }


     