from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from functools import lru_cache

load_dotenv()

class Settings(BaseSettings):
    ENV: str = os.getenv("ENV")
    DATABASE_NAME: str = os.getenv("MONGO_DATABASE_" + os.getenv("ENV"))
    MONGO_URI: str = os.getenv("MONGO_URI_" + os.getenv("ENV"))

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()