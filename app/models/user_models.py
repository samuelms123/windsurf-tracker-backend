from app.config.database import user_collection
from datetime import datetime
from app.utils.exceptions import UserNotFoundError
from pymongo.errors import DuplicateKeyError
from fastapi.responses import JSONResponse
from fastapi import status

def get_user(username: str):
    user = user_collection.find_one(
        {"username": username}
    )
    
    if not user:
        raise UserNotFoundError
    
    return user

def post_user(user:dict):
    try:
        user_collection.insert_one(user)
        return JSONResponse(
            content={"message": "User created"},
            status_code=status.HTTP_201_CREATED
        )
    
    except DuplicateKeyError:
        return JSONResponse(
            content={"error": "Username already exists"},
            status_code=status.HTTP_409_CONFLICT
        )

def set_latest_sync_date(username: str):
    result = user_collection.update_one(
    {"username": username},
    {"$set": {"last_synced": datetime.utcnow()}}
    )
    return result

def update_access_token(new_access_token: str, username: str, expires_at_unix):

    updated_user = user_collection.find_one_and_update(
        {"username": username},
        {"$set": {"access_token": new_access_token,
                  "access_expires_at": expires_at_unix
                  }},
    )

    if not updated_user:
        raise ValueError(f"User '{username}' not found.")

    return updated_user