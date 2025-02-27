from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

secret_key: str = os.getenv("secret_key")
algorithm: str = os.getenv("algorithm")
access_token_expire_minutes: int = int(os.getenv("access_token_expire_minutes", 30))
refresh_token_expire_minutes: int = int(os.getenv("refresh_token_expire_minutes", 3600))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm)
    return encoded_jwt

def verify_jwt(token:str):
    credentials_exception=Exception("Could not verify jwt")
    
    try:
        payload = jwt.decode(token,secret_key,algorithm)
        
        return payload
    
    except JWTError:
        raise credentials_exception
    
