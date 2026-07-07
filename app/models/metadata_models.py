from app.config.database import metadata
import time

def init(access_token: str, expires_at: int):
    metadata.update_one(
        {},
        {
            "$set": 
            {
                "access_token": access_token,
                "expires_at": expires_at,
            }
        },
        upsert=True
    )
    

def get_metadata():
    return metadata.find_one({})

def update_access_token(access_token: str, expires_at: str):
    metadata.update_one(
        {},
        {
            "$set": 
            {
                "access_token": access_token,
                "expires_at": expires_at
            }
        },
        upsert=True
    )

def get_access_token():
    doc = metadata.find_one(
        {},
        {
            "access_token": 1,
            "expires_at": 1,
            "_id": 0
        }
    )

    if doc:
        return doc
    
    return {}

def update_last_synced():
    current_time = int(time.time())
    metadata.update_one(
        {},
        {"$set": {"last_synced": current_time}},
        upsert=True
    )

def get_last_synced():
    doc = metadata.find_one(
        {},
        {""
        "last_synced": 1,
        "_id": 0
        }        
    )

    if doc and "last_synced" in doc:
        return doc["last_synced"]
    
    return None
