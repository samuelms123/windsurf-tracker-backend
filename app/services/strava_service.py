import requests
from app.services import endpoints
from datetime import datetime
from app.config import dotenv

def get_activities(access_token:str) -> dict:
    headers:dict = {'Authorization': f'Authorization: Bearer {access_token}'}
    response = requests.get(endpoints.ACTIVITIES_ENDPOINT, headers=headers)
    response.raise_for_status()
    activity_data = response.json()
    return activity_data

def get_latest_activities(access_token:str) -> dict:

    # 1. Convert date to Unix timestamp
    after_date = datetime(2025, 9, 8)  # YYYY, MM, DD
    after_timestamp = int(after_date.timestamp())

    # 2. Set headers
    access_token = dotenv.STRAVA_ACCESS_TOKEN
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # 3. Set endpoint and parameters
    ACTIVITIES_ENDPOINT = "https://www.strava.com/api/v3/athlete/activities"
    params = {
        "after": after_timestamp,
    }

    # 4. Make the request
    response = requests.get(ACTIVITIES_ENDPOINT, headers=headers, params=params)
    response.raise_for_status()

    # 5. Get JSON data
    activities = response.json()
    return activities

#STREAM_ENDPOINT.format(id=activity_id)
def get_stream_data(access_token:str, activity_id:int) -> dict:
    headers:dict = {'Authorization': f'Authorization: Bearer {access_token}'}
    response = requests.get(endpoints.STREAM_ENDPOINT.format(id=activity_id), headers=headers)
    response.raise_for_status()
    stream_data = response.json()
    return stream_data