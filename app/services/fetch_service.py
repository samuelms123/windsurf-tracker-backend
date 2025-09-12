
import requests
from app.services import endpoints


def get_activity_data(access_token:str, params:dict=None) -> dict:
    headers:dict = {'Authorization': f'Authorization: Bearer {access_token}'}
    if not params:
        response:dict = requests.get(endpoints.ACTIVITIES_ENDPOINT, headers=headers)
    response:dict = requests.get(endpoints.ACTIVITIES_ENDPOINT, headers=headers, params=params)
    response.raise_for_status()
    activity_data = response.json()
    return activity_data