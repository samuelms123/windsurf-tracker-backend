from fastapi import APIRouter
from app.services import strava_service
from app.schemas.activities import Sync
from app.services.auth_service import get_valid_access_token

router = APIRouter(prefix="/strava", tags=["Strava"])

# Fetch activities from Strava 
@router.post("/sync", response_model=Sync)
async def sync_with_strava():
    
    access_token = await get_valid_access_token()
    
    return await strava_service.sync_activities(access_token)
