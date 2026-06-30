from fastapi import APIRouter, Security
from fastapi.security import APIKeyHeader
from app.models import activity_models
from app.config import dotenv
from app.utils.exceptions import InvalidAPIKeyError

router = APIRouter(prefix="/activities", tags=["Activities"])

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

@router.get("")
async def get_synced_activities(
    api_key: str = Security(api_key_header)
):
    if api_key != dotenv.HOME_LAB_API_KEY:
        raise InvalidAPIKeyError
    
    return activity_models.get_analyzed_activities()