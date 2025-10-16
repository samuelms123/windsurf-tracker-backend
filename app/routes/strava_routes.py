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
    # check from database latest synced activity
    latest_sync = models.get_latest_sync_date(username)
    latest_sync = datetime(2025, 10, 2) # for testing
    
    # fetch activites from strava API
    activities = strava_service.get_latest_activities(access_token, latest_sync)
    
    # update latest sync in database
    dbresult = models.set_latest_sync_date(username)
    
    # return if no new activities
    
    
    # extract all the activity id:s (and other info if needed)
    # straight from activites api:
    # date, elapsed time(s), average speed(m/s, maxspeed(m/s), avg heartrate, max heartrate, total distance(m), get location from coordinates
    activity_ids = [activity["id"] for activity in activities]
    
    # get streamdata and analyze
    analysis_results = []
    for id in activity_ids:
        data = strava_service.get_stream_data(access_token, id)
        result = analysis_service.analyze_data(data)
        analysis_results.append(result)
    
    return analysis_results