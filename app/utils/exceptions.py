from fastapi import status

class LoginCredentialException(Exception):
    def __init__(self):
        self.message = "User/password incorrect"
        self.status_code = status.HTTP_401_UNAUTHORIZED