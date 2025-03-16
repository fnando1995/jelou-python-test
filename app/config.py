import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

# some variables are defined in the .env file
class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

settings = Settings()
