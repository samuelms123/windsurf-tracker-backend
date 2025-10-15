from app.config.database import user_collection
from datetime import datetime

def get_latest_sync_date(username: str):
    result = user_collection.find_one(
        {"username": username},
        {"_id": 0, "last_synced": 1}
    )
    
    return result.get("last_synced")


def set_latest_sync_date(username: str):
    result = user_collection.update_one(
    {"username": username},
    {"$set": {"last_synced": datetime.utcnow()}}
    )
    return result