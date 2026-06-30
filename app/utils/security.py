from cryptography.fernet import Fernet
from app.config import dotenv 

def encrypt_token(token: str):
    fernet = Fernet(dotenv.FERNET_SECRET_KEY)
    return fernet.encrypt(token.encode()).decode()

   
def decrypt_token(token: str):
    fernet = Fernet(dotenv.FERNET_SECRET_KEY)
    return fernet.decrypt(token.encode()).decode()

    