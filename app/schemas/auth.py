from pydantic import BaseModel
### pydantic models for auth

class AuthMe(BaseModel):
    refresh_token: str