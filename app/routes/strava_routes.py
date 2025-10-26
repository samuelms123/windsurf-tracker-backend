from fastapi import APIRouter, Security
from app.services import strava_service
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.exceptions import InvalidTokenError
from app.utils.security import decode_jwt_token, decrypt_token
from app.models.user_models import get_user, update_access_token
from app.services import auth_service
from httpx import AsyncClient
import time

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
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    jwt_token = credentials.credentials
    if not jwt_token:
        raise InvalidTokenError()
    payload = decode_jwt_token(jwt_token)
    
    username = payload.get("username")
    if not username:
        raise InvalidTokenError
    
    user = get_user(username)
    access_token = user['access_token']
    expires_at = user['access_expires_at']
    
    current_time = int(time.time())
    
    if not expires_at or current_time >= expires_at:
        encrypted_refresh_token = user['refresh_token']
        refresh_token = decrypt_token(encrypted_refresh_token)
        response = await auth_service.refresh_access_token(refresh_token)
        access_token = response['access_token']
        expires_at = response['expires_at']
        update_access_token(access_token, username, expires_at)
    
        
        
    return await strava_service.sync_activities(access_token, username)


@router.get("/test_refresh")
async def sync_with_strava(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    return await auth_service.refresh_access_token(credentials)