
from app.services import analysis_service, summary_service
from app.models import activity_models, summary_models
from app.schemas import activities as act_schema
from app.utils.exceptions import InvalidTokenError
from app.clients.strava_client import get_latest_activities, verify_strava_response, get_stream_data
from app.services import map_service
import app.models.metadata_models as metadata
     
def filter_windsurf_activities(activities: list[dict]) -> list[dict]:
    windsurf_activities = []
    for activity in activities:
        
        if (
            activity.get("type", "").lower() == "windsurf"
            or activity.get("sport_type", "").lower() == "windsurf"
        ):
            windsurf_activities.append(activity)

            
    return windsurf_activities


async def sync_activities(access_token: str) -> list[dict]:
    
    results = []
    # get user and check from database latest synced activity
    latest_sync = metadata.get_last_synced() 
    
    # fetch activities from strava API
    activities = await get_latest_activities(access_token, latest_sync)
    
    # verify that token was valid
    verify_strava_response(activities, InvalidTokenError())
    
    # Filter windsurf activities
    windsurf_activities = filter_windsurf_activities(activities)
    
    # update latest sync in database
    metadata.update_last_synced()
    
    # return if no new activities
    if not windsurf_activities:
        return {
        "activities": [],
        "updated_summary": None
    }
    
    # get streamdata and analyze
    for activity in windsurf_activities:
        try:
            
            da = analysis_service.DataAnalysis()
            data = await get_stream_data(access_token, activity['id'])
            print("Data fetched from strava")
            result = da.analyze_data(data)
            start_location = map_service.get_location(activity["start_latlng"][0], activity["start_latlng"][1])
            
            result.update({
            'strava_id': activity['id'],
            'date': activity['start_date'],
            'start_location': start_location,
            'elapsed_time': activity['elapsed_time'],
            'average_speed': activity['average_speed'],
            'max_speed': activity['max_speed'],
            'total_distance': activity['distance'],
            })
            # location from activity['start_latlng']
            
            results.append(result)
            print("Data analyzed")
        except Exception as e:
            print(f"Error processing activity with id: {activity['id']}")
            
    # save analysis to database
    activity_models.save_analyzed_activities(results)

    summary = summary_service.calculate_summary(results)
    updated_summary = summary_models.update_summary(summary)
    
    for activity in results:
        act_schema.serialize_activity(activity)
    
    
    return {
        "activities": results,
        "updated_summary": updated_summary
    }
