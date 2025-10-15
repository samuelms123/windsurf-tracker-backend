from fastapi import status

class LoginCredentialError(Exception):
    def __init__(self):
        self.message = "User/password incorrect"
        self.status_code = status.HTTP_401_UNAUTHORIZED
        

class InvalidTokenError(Exception):
    def __init__(self):
        self.message = "Invalid token"
        self.status_code = status.HTTP_401_UNAUTHORIZED