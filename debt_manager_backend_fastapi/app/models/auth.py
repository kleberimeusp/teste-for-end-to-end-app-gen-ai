from pydantic import BaseModel, EmailStr

class UserRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    username: str
    name: str
    email: str
    password: str
    
