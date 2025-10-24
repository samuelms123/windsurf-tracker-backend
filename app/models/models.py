from app.config.database import user_collection, activity_collection
from datetime import datetime
from bson import ObjectId

async def get_user(username: str):
    user = user_collection.find_one(
        {"username": username}
    )
    
    return user


async def set_latest_sync_date(username: str):
    result = user_collection.update_one(
    {"username": username},
    {"$set": {"last_synced": datetime.utcnow()}}
    )
    return result

async def save_analyzed_activities(activities: list[dict]):
    activity_collection.insert_many(activities) 
        
    
    