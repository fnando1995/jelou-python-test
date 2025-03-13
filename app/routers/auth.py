from fastapi import APIRouter, HTTPException, Depends
from models import CreateUserRequest, Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Annotated
from starlette.status import HTTP_201_CREATED
from database import save_user, load_user
from security import pwd_context,create_access_token

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from config import settings

auth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/",status_code=HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest):
    save_user({
                "username":[create_user_request.username],
                "hashed_password":[pwd_context.hash(create_user_request.password)]
                })
    return {"message":"User created successfully"}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()]):
    user_data = load_user({"username":form_data.username})
    if not user_data:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not pwd_context.verify(form_data.password, user_data.get("hashed_password")):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return Token(access_token=create_access_token(data=user_data.get("username")))#,token_type="bearer"

async def get_current_user(token: Token = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user