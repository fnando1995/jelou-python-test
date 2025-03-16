from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.status import HTTP_201_CREATED
import jwt
from config import settings
from database import save_user, load_user
from models import CreateUserRequest, Token, User
from datetime import datetime, timedelta
from typing import Optional, Annotated
from passlib.context import CryptContext
from logger import get_logger

# hash password helper
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# object to obtain token from header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_password_hash(password: str)-> str:
    """Hash the password using bcrypt."""
    return pwd_context.hash(password)

def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None)-> str:
    """Create an access token with the user data."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme),logger=Depends(get_logger))-> User:
    """Get the current user from the token."""
    credentials_exception = HTTPException(
                                            status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail="Could not validate credentials",
                                            headers={"WWW-Authenticate": "Bearer"},
                                        )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.error("Token does not contain username")
            raise credentials_exception
    except Exception:

        raise credentials_exception
    user = load_user({"username":username})
    if user is None:
        logger.error("User not found")
        raise credentials_exception
    user = User(**user)
    return user



router = APIRouter()

@router.post("/",status_code=HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest,logger = Depends(get_logger)):
    """Register a new user in the database."""
    save_user({
                "username":[create_user_request.username],
                "hashed_password":[pwd_context.hash(create_user_request.password)]
                })
    return {"message":"User created successfully"}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],logger = Depends(get_logger)):
    """Login and return an access token."""
    user_data = load_user({"username":form_data.username})
    if not user_data:
        logger.error(f"User {form_data.username} not found")
        raise HTTPException(status_code=401, detail="No user in database")
    if not pwd_context.verify(form_data.password, user_data.get("hashed_password")):
        logger.error(f"User {form_data.username} provided incorrect password")
        raise HTTPException(status_code=401, detail="Incorrect password")
    username = user_data.get("username")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}