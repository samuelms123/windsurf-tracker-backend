from fastapi import APIRouter, Security
from app.services import strava_service
from app.utils.exceptions import InvalidAPIKeyError
from fastapi.security import APIKeyHeader
from app.config import dotenv
from app.schemas.activities import Sync
from app.services.auth_service import get_valid_access_token

router = APIRouter(prefix="/strava", tags=["Strava"])

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


# Fetch activities from Strava 
@router.get("/sync", response_model=Sync)
async def sync_with_strava(
    api_key: str = Security(api_key_header)
):
    if api_key != dotenv.HOME_LAB_API_KEY:
        raise InvalidAPIKeyError
    
    access_token = await get_valid_access_token()
    
    return await strava_service.sync_activities(access_token)


'''
@router.get("/test_refresh")
async def sync_with_strava(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    return await auth_service.refresh_access_token(credentials)
'''