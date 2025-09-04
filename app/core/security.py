from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"] , deprecated = "auto")

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain:str , hashed:str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(sub:str , expires_minutes:int | None = None) -> str:
    now = datetime.now(tz=timezone.utc)
    exp_minutes = expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = now + timedelta(minutes=exp_minutes)

    payload = {
        "sub" : sub,
        "exp" : int(expire.timestamp()),
        "iat" : int(now.timestamp()),
        "nbf" : int(now.timestamp())
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise JWTError("Invalid token")

