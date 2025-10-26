from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from app.config import dotenv
from datetime import datetime, timedelta
import os
import jwt
from fastapi import HTTPException, status

ph = PasswordHasher()

def hash_password(password: str):
    return ph.hash(password)


def verify_password(hashed_password: str, password: str):
    try:
        ph.verify(hashed_password, password)
        return True
    
    except Exception:
        return False
    

def encrypt_token(token: str):
    fernet = Fernet(os.getenv("REFRESH_TOKEN_SECRET_KEY"))
    return fernet.encrypt(token.encode()).decode()
   
def decrypt_token(token: str):
    fernet = Fernet(os.getenv("REFRESH_TOKEN_SECRET_KEY"))
    return fernet.decrypt(token.encode()).decode()

def create_jwt_token_for_database(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=dotenv.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, dotenv.JWT_SECRET_KEY, algorithm=dotenv.JWT_ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token: str, verify_exp: bool = True):
    try:
        payload = jwt.decode(
            token,
            dotenv.JWT_SECRET_KEY,
            algorithms=[dotenv.JWT_ALGORITHM],
            options={"verify_exp": verify_exp}
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT token has expired",
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT token",
        )
    