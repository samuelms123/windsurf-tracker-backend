from fastapi import status
        

class InvalidTokenError(Exception):
    def __init__(self):
        self.message = "Invalid Strava access token"
        self.status_code = status.HTTP_401_UNAUTHORIZED


class InvalidAPIKeyError(Exception):
    def __init__(self):
        self.message = "Invalid API key"
        self.status_code = status.HTTP_401_UNAUTHORIZED