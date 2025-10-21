import requests
from app.services import endpoints
from datetime import datetime
from app.config import dotenv
from app.services import analysis_service
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


async def sync_activities(access_token: str, username: str):
    
    results = []
    
    # check from database latest synced activity
    ##latest_sync = models.get_latest_sync_date(username)
    ##latest_sync = datetime(2025, 9, 21) # for testing
    latest_sync = None ## for testing
    
    # fetch activities from strava API
    activities = get_latest_activities(access_token, latest_sync)
    
    # update latest sync in database
    ##dbresult = models.set_latest_sync_date(username)
    
    # return if no new activities
    
    
    # get streamdata and analyze

    for activity in activities:
        try:
            
            da = analysis_service.DataAnalysis()
            data = get_stream_data(access_token, activity['id'])
            print("Data fetched from strava")
            result = da.analyze_data(data)
            
            result.update({
            'date': activity['start_date'],
            'elapsed_time': activity['elapsed_time'],
            'average_speed': activity['average_speed'],
            'max_speed': activity['max_speed'],
            'total_distance': activity['distance'],
            })
            # location from activity['start_latlng']
            
            results.append(result)
            print("Data analyzed")
        except Exception as e:
            print(f"Error processing activity with id: {activity['id']}")
    
    return results