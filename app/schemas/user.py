from pydantic import BaseModel, EmailStr

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str | None = None
    full_name: str | None = None
    is_active: bool
    is_admin: bool
    
    class Config:
        from_attributes = True
