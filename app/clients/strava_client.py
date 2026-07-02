import httpx
from httpx import AsyncClient
from fastapi import HTTPException
from typing import Optional
from app.utils import endpoints
from app.config import dotenv

## Responsible for communicating with Strava API


def verify_strava_response(response, error: Exception) -> None:
    if isinstance(response, dict) and response.get('message') == 'Authorization Error':
        raise error


async def get_latest_activities(access_token:str, last_synced: Optional[int]) -> list[dict]:
    params = {}
    
    if last_synced is not None:
        params["after"] = last_synced
    
     
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        async with AsyncClient(timeout=30) as client:
            response = await client.get("https://www.strava.com/api/v3/athlete/activities", headers=headers, params=params)
            response.raise_for_status()
            activities = response.json()
            return activities
    except httpx.RequestError:
        raise HTTPException(status_code=504, detail="Request to Strava timed out")
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Strava API error: {str(e)}")
    

async def get_stream_data(access_token:str, activity_id:int) -> list[dict]:
    headers:dict = {
        'Authorization': f'Bearer {access_token}'
     }
    
    params:dict = {
        "keys": "time,latlng,velocity_smooth,distance"
    }
    
    url = endpoints.STREAM_ENDPOINT.format(id=activity_id)
    try:
        async with AsyncClient(timeout=30) as client:
            
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            stream_data = response.json()
            return stream_data
    except httpx.RequestError:
        raise HTTPException(status_code=504, detail="Request to Strava timed out")
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Strava API error: {str(e)}")
    

async def refresh_access_token() -> str:
    payload:dict = {
    'client_id': dotenv.STRAVA_CLIENT_ID,
    'client_secret': dotenv.STRAVA_CLIENT_SECRET,
    'refresh_token': dotenv.STRAVA_REFRESH_TOKEN,
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