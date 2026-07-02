from fastapi import APIRouter, Security
from app.services import strava_service
import app.models.metadata_models as metadata
from app.services import auth_service
import time
from app.utils.exceptions import InvalidAPIKeyError
from fastapi.security import APIKeyHeader
from app.config import dotenv
from app.schemas.activities import Activity

router = APIRouter(prefix="/strava", tags=["Strava"])

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


# Fetch activities from Strava 
@router.get("/sync", response_model=list[Activity])
async def sync_with_strava(
    api_key: str = Security(api_key_header)
):
    if api_key != dotenv.HOME_LAB_API_KEY:
        raise InvalidAPIKeyError
    
    current_time = int(time.time())
    token = metadata.get_access_token()
    access_token = token.get("access_token")
    
    if not token.get("expires_at") or current_time >= token.get("expires_at"):
        response = await auth_service.refresh_access_token()
        new_access_token = response['access_token']
        expires_at = response['expires_at']
        access_token = new_access_token
        metadata.update_access_token(new_access_token, expires_at)
    
        
        
    return await strava_service.sync_activities(access_token)


'''
@router.get("/test_refresh")
async def sync_with_strava(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    return await auth_service.refresh_access_token(credentials)
'''