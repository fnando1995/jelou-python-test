# from fastapi import HTTPException, Header
# import jwt
# from config import settings
# from datetime import datetime, timedelta

# def verify_token(authorization: str = Header(...)):
#     try:
#         scheme, _, token = authorization.partition(" ")
#         if scheme.lower() != "bearer":
#             raise HTTPException(status_code=401, detail="Invalid auth scheme")
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         return payload
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid token")

# def create_jwt(user_id: str):
#     """Generate a JWT token for a given user ID."""
#     expiration = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     payload = {"sub": user_id, "exp": expiration}
#     token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#     return token
from datetime import datetime, timedelta
from typing import Optional
from config import settings
import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt