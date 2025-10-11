from fastapi import APIRouter
from app.schemas.user import User, list_serial
from app.config.database import user_collection
from bson import ObjectId

router = APIRouter(prefix="/users", tags=["users"])

### User/Database related routes

@router.get("")
async def get_users():
    users = list_serial(user_collection.find())
    return users


@router.post("")
async def post_user(user: User):
    user_collection.insert_one(dict(user))

