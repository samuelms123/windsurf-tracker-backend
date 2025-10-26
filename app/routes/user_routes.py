from fastapi import APIRouter, status
from app.schemas.user import User, list_serial, Username
from app.models.user_models import get_user, post_user
from app.utils import security
from app.utils.exceptions import UserAlreadyTakenError, UserNotFoundError

router = APIRouter(prefix="/users", tags=["Users"])

### User/Database related routes
'''
@router.get("")
async def get_users():
    users = list_serial(user_collection.find())
    return users
'''

@router.post("")
async def post_user_to_db(user: User):
    hashed_pass: str = security.hash_password(user.password)
    encrypted_token = security.encrypt_token(user.refresh_token)
    user.password = hashed_pass
    user.refresh_token = encrypted_token
    user_dict = dict(user)
    return post_user(user_dict)
    
@router.get("/available")
async def check_if_username_is_available(username: str):
    user = get_user(username)
    if user:
        raise UserAlreadyTakenError
