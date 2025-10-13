from pydantic import BaseModel
### pydantic models for user

class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    
def list_serial(users) -> list:
    return[individual_serial(user) for user in users]

def individual_serial(user: User) -> dict:
    return {
        "id": str(user["_id"]),
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "username": user["username"],
        "password": user["password"], 
    }