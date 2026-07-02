from fastapi import APIRouter, Security
from fastapi.security import APIKeyHeader
from app.models import activity_models
from app.config import dotenv
from app.utils.exceptions import InvalidAPIKeyError
from app.schemas.activities import Activity, Summary

router = APIRouter(prefix="/activities", tags=["Activities"])

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

@router.get("", response_model=list[Activity])
async def get_synced_activities(
    api_key: str = Security(api_key_header)
):
    if api_key != dotenv.HOME_LAB_API_KEY:
        raise InvalidAPIKeyError
    
    return activity_models.get_analyzed_activities()


@router.get("/summary", response_model=Summary)
async def get_activity_summary(
        api_key: str = Security(api_key_header)
):
    if api_key != dotenv.HOME_LAB_API_KEY:
        raise InvalidAPIKeyError
    
    return activity_models.get_activity_summary()
    
