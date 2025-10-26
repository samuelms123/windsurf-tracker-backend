from fastapi import APIRouter, Security
from app.models import activity_models
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.exceptions import InvalidTokenError
from app.utils.security import decode_jwt_token

router = APIRouter(prefix="/activities", tags=["Activities"])
bearer_scheme = HTTPBearer()

@router.get("")
async def get_synced_activities(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    jwt_token = credentials.credentials
    if not jwt_token:
        raise InvalidTokenError()
    payload = decode_jwt_token(jwt_token)
    
    username = payload.get("username")
    if not username:
        raise InvalidTokenError
    
    return activity_models.get_analyzed_activities(username)