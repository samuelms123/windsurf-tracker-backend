from fastapi import APIRouter
from app.services import strava_service

router = APIRouter(prefix="/strava", tags=["strava"])

@router.get("/auth/me")
async def me(refresh_token: str):
    access_token = strava_service.get_access_token()
    return {"access_token": access_token}

## RETURN ONLY WHAT U WANT TO DISPLAY IN FRONTEND! SO PROBABLY NOT THESE, OR MAYBE ACTIVITIES
@router.get("/activities")
async def get_activities(access_token: str):
    activities = strava_service.get_activities(access_token)
    return activities

@router.get("/streams/{activity_id}")
async def get_streams(activity_id: int, access_token: str):
    stream = strava_service.get_stream_data(access_token, activity_id)
    ### Need to analyze data
    return None
