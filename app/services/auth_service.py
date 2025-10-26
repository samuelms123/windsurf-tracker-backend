import httpx
from httpx import AsyncClient
from app.utils import endpoints
from app.config import dotenv
from fastapi import HTTPException

async def get_access_token() -> str:
    payload:dict = {
    'client_id': dotenv.STRAVA_CLIENT_ID,
    'client_secret': dotenv.STRAVA_CLIENT_SECRET,
    'refresh_token': dotenv.MY_REFRESH_TOKEN,
    'grant_type': "access_token"
    }
    try:
        async with AsyncClient(timeout=30) as client:
            res = await client.post(endpoints.AUTH_ENDPOINT, data=payload)
            access_token = res.json()
            return access_token
    except httpx.RequestError:
        raise HTTPException(status_code=504, detail="Request to Strava timed out")

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Strava API error: {str(e)}")

async def refresh_access_token(refresh_token: str) -> str:
    payload:dict = {
    'client_id': dotenv.STRAVA_CLIENT_ID,
    'client_secret': dotenv.STRAVA_CLIENT_SECRET,
    'refresh_token': refresh_token,
    'grant_type': "refresh_token",
    }
    try:
        async with AsyncClient(timeout=30) as client:
            res = await client.post(endpoints.AUTH_ENDPOINT, data=payload)
            res.raise_for_status() 
            return res.json()
    except httpx.RequestError:
        raise HTTPException(status_code=504, detail="Request to Strava timed out")

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Strava API error: {str(e)}")