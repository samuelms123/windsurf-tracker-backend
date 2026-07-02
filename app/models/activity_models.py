from app.config.database import activity_collection
from app.schemas.activities import serialize_activity
### Synced activity related DB logic

def save_analyzed_activities(activities: list[dict]):
    for activity in activities:
        strava_id = activity.get("id")
        
        if not strava_id:
            print(f"Skipping an activity because it is missing an 'id' key. Keys present: {list(activity.keys())}")
            continue
            
        activity_collection.update_one(
            {"id": strava_id}, 
            {"$set": activity}, 
            upsert=True
        )

def get_analyzed_activities():
    activities = list(activity_collection.find())
    
    if not activities:
        return {'message': 'no activities found in database'}
    
    
    for activity in activities:
        serialize_activity(activity)
        
    return activities