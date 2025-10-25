import requests
from app.utils import endpoints
from datetime import datetime
from app.config import dotenv
from app.services import analysis_service
from app.models import user_models, activity_models
from datetime import datetime
from app.schemas import activities as act_schema
from app.utils.exceptions import InvalidTokenError
from fastapi import HTTPException
from app.services import map_service
import time

async def verify_strava_response(response, error: Exception):
    if isinstance(response, dict) and response.get('message') == 'Authorization Error':
        raise error
    return response

def get_activities(access_token:str) -> dict:
    headers:dict = {'Authorization': f'Authorization: Bearer {access_token}'}
    try:
        response = requests.get(endpoints.ACTIVITIES_ENDPOINT, headers=headers, timeout=30)
        response.raise_for_status()
        activity_data = response.json()
        return activity_data
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Request to Strava timed out")
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Strava API error: {str(e)}")

async def get_latest_activities(access_token:str, last_synced: datetime) -> dict:
    params = {}
    
    if last_synced is not None:
        after_timestamp = int(time.mktime(last_synced.timetuple()))
        params["after"] = after_timestamp

    ## after_date = datetime(2025, 10, 2)  # YYYY, MM, DD
    
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get("https://www.strava.com/api/v3/athlete/activities", headers=headers, params=params, timeout=30)
        response.raise_for_status()
        activities = response.json()
        return activities
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Request to Strava timed out")
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Strava API error: {str(e)}")
        
async def filter_windsurf_activities(activities):
    windsurf_activities = []
    for activity in activities:
        
        if (
            activity.get("type", "").lower() == "windsurf"
            or activity.get("sport_type", "").lower() == "windsurf"
        ):
            windsurf_activities.append(activity)
            
    return windsurf_activities
            
    
    

async def get_stream_data(access_token:str, activity_id:int) -> dict:
    headers:dict = {
        'Authorization': f'Authorization: Bearer {access_token}'
     }
    
    params:dict = {
        "keys": "time,latlng,velocity_smooth,distance"
    }
    
    url = endpoints.STREAM_ENDPOINT.format(id=activity_id)
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        stream_data = response.json()
        return stream_data
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Request to Strava timed out")
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Strava API error: {str(e)}")


async def sync_activities(access_token: str, username: str):
    
    results = []
    
    # get user and check from database latest synced activity
    user = await user_models.get_user(username)
    latest_sync = user['last_synced']
    user_id = user['_id']  
    
    # fetch activities from strava API
    activities = await get_latest_activities(access_token, latest_sync)
    
    # verify that token was valid
    await verify_strava_response(activities, InvalidTokenError)
    
    # Filter windsurf activities
    windsurf_activities = await filter_windsurf_activities(activities)
    
    # update latest sync in database
    await user_models.set_latest_sync_date(username)
    
    # return if no new activities
    if not windsurf_activities:
        return ({'message': 'No new windsurf activities detected'})
    
    # get streamdata and analyze
    for activity in windsurf_activities:
        try:
            
            da = analysis_service.DataAnalysis()
            data = await get_stream_data(access_token, activity['id'])
            print("Data fetched from strava")
            result = da.analyze_data(data)
            start_location = await map_service.get_location(activity["start_latlng"][0], activity["start_latlng"][1])
            
            result.update({
            'user_id': user_id,
            'date': activity['start_date'],
            'start_location': start_location,
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
            
    # save analysis to database
    await activity_models.save_analyzed_activities(results)
    
    for activity in results:
        act_schema.serialize_activity(activity)
    
    
    return results
