from argon2 import PasswordHasher, exceptions

ph = PasswordHasher()

def hashPassword(password: str):
    return ph.hash(password)


def verifyPassword(hashed_password: str, password: str):
    try:
        ph.verify(hashed_password, password)
        return True
    
    except Exception as e:
        return False
    