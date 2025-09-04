from fastapi import Depends, HTTPException, status, Cookie, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import verify_token
from app.models.user import User
from jose import JWTError

# Make Authorization header optional so cookie-based auth works without using Swagger's Authorize modal
security = HTTPBearer(auto_error=False)

async def get_current_user(
    db: Session = Depends(get_db),
    access_token: str = Cookie(None),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = None
    
    # Try to get token from cookie first
    if access_token:
        token = access_token
    # Fall back to Authorization header
    elif credentials:
        token = credentials.credentials
    
    if not token:
        raise credentials_exception
    
    try:
        payload = verify_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_user_optional(
    request: Request,
    db: Session = Depends(get_db)
) -> User | None:
    """Get current user if authenticated, otherwise return None"""
    try:
        # Try to get token from cookie
        access_token = request.cookies.get("access_token")
        if not access_token:
            return None
        
        payload = verify_token(access_token)
        email: str = payload.get("sub")
        if email is None:
            return None
        
        user = db.query(User).filter(User.email == email).first()
        return user
    except:
        return None


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
