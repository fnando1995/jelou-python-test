from fastapi import APIRouter, HTTPException, Depends
from models import CreateUserRequest, Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from dependencies import create_jwt, verify_token
from typing import Annotated
from starlette.status import HTTP_201_CREATED
from database import save_user, load_user

router = APIRouter()
bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/",status_code=HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest):
    save_user({
                "username":[create_user_request.username],
                "hashed_password":[bcrypt.hash(create_user_request.password)]
                })
    return {"message":"User created successfully"}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()]):
    print(form_data)
    user_data = load_user({"username":form_data.username})
    if not user_data:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not bcrypt.verify(form_data.password, user_data.get("hashed_password")):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return Token(access_token=create_jwt(user_data.get("username")),
                token_type="bearer")
