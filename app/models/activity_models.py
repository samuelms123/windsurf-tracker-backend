from app.config.database import activity_collection
from app.models import user_models
from app.schemas.activities import serialize_activity
### Synced activity related DB logic

def save_analyzed_activities(activities: list[dict]):
    activity_collection.insert_many(activities) 

def get_analyzed_activities(username: str):
    user = user_models.get_user(username)
    user_id = user['_id']
    
    activities = list(activity_collection.find({"user_id": user_id}))
    
    if not activities:
        return {'message: no activities found in database'}
    
    for activity in activities:
        serialize_activity(activity)
        
    return activities