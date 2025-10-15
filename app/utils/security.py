from argon2 import PasswordHasher
from cryptography.fernet import Fernet
import os

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