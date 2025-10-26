import httpx, requests
from httpx import AsyncClient
from app.utils import endpoints
from app.config import dotenv

def get_access_token() -> str:
    payload:dict = {
    'client_id': dotenv.STRAVA_CLIENT_ID,
    'client_secret': dotenv.STRAVA_CLIENT_SECRET,
    'refresh_token': dotenv.MY_REFRESH_TOKEN,
    'grant_type': "access_token",
    'f': 'json'
    }
    res = requests.post(endpoints.AUTH_ENDPOINT, data=payload, timeout=30)
    access_token = res.json()
    return access_token

async def refresh_access_token(refresh_token: str) -> str:
    payload:dict = {
    'client_id': dotenv.STRAVA_CLIENT_ID,
    'client_secret': dotenv.STRAVA_CLIENT_SECRET,
    'refresh_token': refresh_token, ## config.MY_REFRESH_TOKEN for testing
    'grant_type': "refresh_token",
    }
    
    async with AsyncClient() as client:
        res = await client.post(endpoints.AUTH_ENDPOINT, data=payload)
        res.raise_for_status() 
        return res.json()