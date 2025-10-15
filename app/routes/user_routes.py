from fastapi import APIRouter
from app.schemas.user import User, list_serial, Username
from app.config.database import user_collection
from app.utils import security

router = APIRouter(prefix="/users", tags=["Users"])

### User/Database related routes

@router.get("")
async def get_users():
    users = list_serial(user_collection.find())
    return users


@router.post("")
async def post_user(user: User):
    hashed_pass: str = security.hash_password(user.password)
    encrypted_token = security.encrypt_token(user.refresh_token)
    user.password = hashed_pass
    user.refresh_token = encrypted_token
    user_collection.insert_one(dict(user))
    
@router.get("/available")
async def check_if_username_is_available(username: str):
    user = user_collection.find_one({"username": username})
    if user:
        return {"message": "unavailable"}
    return {"message": "available"}

