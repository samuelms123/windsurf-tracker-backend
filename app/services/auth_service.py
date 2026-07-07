import time
from app.clients.strava_client import refresh_access_token
from app.models.metadata_models import get_access_token, update_access_token

async def get_valid_access_token() -> str:
    current_time = int(time.time())
    token = get_access_token()
    access_token = token.get("access_token")
    
    if not token.get("expires_at") or current_time >= token.get("expires_at"):
        response = await refresh_access_token()
        new_access_token = response['access_token']
        expires_at = response['expires_at']
        access_token = new_access_token
        update_access_token(new_access_token, expires_at)
    
    return access_token