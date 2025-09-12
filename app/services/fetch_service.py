
import requests
from app.services import endpoints


def get_activity_data(access_token:str) -> dict:
    headers:dict = {'Authorization': f'Authorization: Bearer {access_token}'}
    response = requests.get(endpoints.ACTIVITIES_ENDPOINT, headers=headers)
    response.raise_for_status()
    activity_data = response.json()
    return activity_data

#STREAM_ENDPOINT.format(id=activity_id)
def get_stream_data(access_token:str, activity_id:int) -> dict:
    headers:dict = {'Authorization': f'Authorization: Bearer {access_token}'}
    response = requests.get(endpoints.STREAM_ENDPOINT.format(id=activity_id), headers=headers)
    response.raise_for_status()
    stream_data = response.json()
    return stream_data
