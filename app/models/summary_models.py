from app.config.database import activity_summary
from app.schemas.activities import Summary
from pymongo import ReturnDocument

def get_summary():
    return activity_summary.find_one({})

def update_summary(summary: Summary):
    if not summary:
        return
    
    updated_doc = activity_summary.find_one_and_update(
        {},
        {
            "$inc": {
                "total_distance": summary.total_distance,
                "time_spent": summary.time_spent,
                "time_spent_planing": summary.time_spent_planing,
                "total_session_count": summary.total_session_count
            },

            "$max": {
                "top_speed": summary.top_speed
            },
            "$min": {
                "fastest_100": summary.fastest_100,
                "fastest_500": summary.fastest_500,
                "fastest_1000": summary.fastest_1000
            }
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
        projection={"_id": 0}
    )

    return updated_doc