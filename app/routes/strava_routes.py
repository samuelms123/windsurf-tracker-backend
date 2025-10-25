from fastapi import APIRouter, Security
from app.services import strava_service
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.exceptions import InvalidTokenError

router = APIRouter(prefix="/strava", tags=["Strava"])
bearer_scheme = HTTPBearer()
'''
@router.get("/activities")
async def get_activities(access_token: str):
    activities = strava_service.get_activities(access_token)
    return activities

@router.get("/streams")
async def get_streams(activity_id: int, access_token: str):
    stream = strava_service.get_stream_data(access_token, activity_id)
    ### Need to analyze data
    return stream
'''

@router.get("/sync")
async def sync_with_strava(
    username: str,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    token = credentials.credentials
    if not token:
        raise InvalidTokenError()
    
    return await strava_service.sync_activities(token, username)