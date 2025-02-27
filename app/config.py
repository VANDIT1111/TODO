from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


load_dotenv()

class Settings(BaseSettings):
    database_hostname: str = os.getenv("database_hostname")
    database_port: str = os.getenv("database_port")
    database_password: str = os.getenv("database_password")
    database_name: str = os.getenv("database_name")
    database_username: str = os.getenv("database_username")
    secret_key: str = os.getenv("secret_key")
    algorithm: str = os.getenv("algorithm")
    access_token_expire_minutes: int = int(os.getenv("access_token_expire_minutes", 30))
    refresh_token_expire_minutes: int = int(os.getenv("refresh_token_expire_minutes", 3600))
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()


