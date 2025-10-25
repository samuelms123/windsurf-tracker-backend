from fastapi import status

class LoginCredentialError(Exception):
    def __init__(self):
        self.message = "User/password incorrect"
        self.status_code = status.HTTP_401_UNAUTHORIZED
        

class InvalidTokenError(Exception):
    def __init__(self):
        self.message = "Invalid Strava access token"
        self.status_code = status.HTTP_401_UNAUTHORIZED
        

class UserNotFoundError(Exception):
    def __init__(self):
        self.message = "User not found"
        self.status_code = status.HTTP_404_NOT_FOUND
        

class UserAlreadyTakenError(Exception):
    def __init__(self):
        self.message = "Username already taken"
        self.status_code = status.HTTP_409_CONFLICT