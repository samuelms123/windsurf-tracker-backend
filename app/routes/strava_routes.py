from fastapi import APIRouter
from app.services import strava_service
from app.models import models
from datetime import datetime
from app.services import analysis_service

router = APIRouter(prefix="/strava", tags=["Strava"])


## RETURN ONLY WHAT U WANT TO DISPLAY IN FRONTEND! SO PROBABLY NOT THESE, OR MAYBE ACTIVITIES
@router.get("/activities")
async def get_activities(access_token: str):
    activities = strava_service.get_activities(access_token)
    return activities

@router.get("/streams")
async def get_streams(activity_id: int, access_token: str):
    stream = strava_service.get_stream_data(access_token, activity_id)
    ### Need to analyze data
    return stream

@router.get("/sync")
async def sync_with_strava(access_token: str, username: str):
    results = []
    
    # check from database latest synced activity
    ##latest_sync = models.get_latest_sync_date(username)
    ##latest_sync = datetime(2025, 9, 21) # for testing
    latest_sync = None ## for testing
    
    # fetch activities from strava API
    activities = strava_service.get_latest_activities(access_token, latest_sync)
    
    # update latest sync in database
    ##dbresult = models.set_latest_sync_date(username)
    
    # return if no new activities
    
    
    # get streamdata and analyze

    for activity in activities:
        da = analysis_service.DataAnalysis()
        data = strava_service.get_stream_data(access_token, activity['id'])
        print("Data fetched from strava")
        result = da.analyze_data(data)
        
        result['date'] = activity['start_date']
        result['elapsed_time'] = activity['elapsed_time']
        result['average_speed'] = activity['average_speed']
        result['max_speed'] = activity['max_speed']
        result['total_distance'] = activity['distance']
        # location from activity['start_latlng']
        
        results.append(result)
        print("Data analyzed")
    
    return results