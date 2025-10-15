import requests
from app.services import endpoints
from datetime import datetime
from app.config import dotenv
import time

def get_activities(access_token:str) -> dict:
    headers:dict = {'Authorization': f'Authorization: Bearer {access_token}'}
    response = requests.get(endpoints.ACTIVITIES_ENDPOINT, headers=headers)
    response.raise_for_status()
    activity_data = response.json()
    return activity_data

def get_latest_activities(access_token:str, last_synced: datetime) -> dict:
    params = {}
    
    if last_synced is not None:
        after_timestamp = int(time.mktime(last_synced.timetuple()))
        params["after"] = after_timestamp

    ## after_date = datetime(2025, 10, 2)  # YYYY, MM, DD
    
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get("https://www.strava.com/api/v3/athlete/activities", headers=headers, params=params)

    activities = response.json()
    return activities

def get_stream_data(access_token:str, activity_id:int) -> dict:
    headers:dict = {
        'Authorization': f'Authorization: Bearer {access_token}'
     }
    
    params:dict = {
        "keys": "time,latlng,velocity_smooth,distance"
    }
    
    url = endpoints.STREAM_ENDPOINT.format(id=activity_id)
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    stream_data = response.json()
    return stream_data