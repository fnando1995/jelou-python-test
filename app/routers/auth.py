
from fastapi import APIRouter, HTTPException, Depends
from models import CreateUserRequest, Token

router = APIRouter()

@router.post("/")
async def create_user():
    pass