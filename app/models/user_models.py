from app.config.database import user_collection
from datetime import datetime

async def get_user(username: str):
    user = user_collection.find_one(
        {"username": username}
    )
    
    if not user:
        return {f'message: no users found by username: "{username}" '}
    
    return user


async def set_latest_sync_date(username: str):
    result = user_collection.update_one(
    {"username": username},
    {"$set": {"last_synced": datetime.utcnow()}}
    )
    return result
        
    
    