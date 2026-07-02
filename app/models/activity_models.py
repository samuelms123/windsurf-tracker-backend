from app.config.database import activity_collection
from app.schemas.activities import serialize_activity
### Synced activity related DB logic

def save_analyzed_activities(activities: list[dict]):
    if not activities:
        return
    
    for activity in activities:
        strava_id = activity.get("strava_id")
        
        if not strava_id:
            print(f"Skipping an activity because it is missing an 'id' key.")
            continue

        activity["_id"] = str(strava_id)
            
        activity_collection.update_one(
            {"_id": activity["_id"]}, 
            {"$set": activity}, 
            upsert=True
        )

def get_analyzed_activities():
    activities = list(activity_collection.find())
    
    if not activities:
        return []
    
    
    for activity in activities:
        serialize_activity(activity)
        
    return activities

def get_activity_summary():
    pass