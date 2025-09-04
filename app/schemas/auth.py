from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr  # Changed from username to email to match the service
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    is_active: bool
    is_admin: bool
    
    class Config:
        from_attributes = True
