from fastapi import APIRouter
from app.services import strava_service
from app.models import models

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
    
    # fetch from strava API
    result = strava_service.get_latest_activities(access_token, latest_sync)
    
    # update latest sync in database
    dbresult = models.set_latest_sync_date(username)
    
    
    return result
    # get activities after x date
    # if acticities found:
    # get streams from strava api with the activity ids
    # do anylysing on the data
    #return results
