from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, Token
from app.schemas.user import UserOut
from app.services.auth_service import register_user, login_user, make_user_admin
from app.core.security import create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, payload.email, payload.username, payload.full_name, payload.password)
    return user


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = login_user(db, payload.email, payload.password)
    
    # Create token
    token = create_access_token(sub=user.email)
    
    # Set cookie for automatic authentication
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax"
    )
    
    return {"access_token": token, "token_type": "bearer"}


@router.post("/make-admin/{user_id}")
def make_admin(user_id: int, db: Session = Depends(get_db)):
    user = make_user_admin(db, user_id)
    return {"message": f"User {user.email} is now an admin"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}