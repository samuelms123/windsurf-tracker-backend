from pydantic import BaseModel
from typing import Optional
from datetime import datetime
### pydantic models for user

class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    refresh_token: str
    access_token: Optional[str] = None
    access_expires_at: Optional[datetime] = None
    last_synced: Optional[datetime] = None
    
class Username(BaseModel):
    username: str
    
def list_serial(users) -> list:
    return[individual_serial(user) for user in users]

def individual_serial(user: User) -> dict:
    return {
        "id": str(user["_id"]),
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "username": user["username"],
        "password": user["password"],
        "refresh_token": user["refresh_token"],
        "access_token": user["access_token"],
        "access_expires_at": user["access_expires_at"],
        "last_synced": user["last_synced"]
    }