from fastapi import APIRouter
from app.services import strava_service
from app.models import models
from datetime import datetime

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
    return await strava_service.sync_activities(access_token, username)