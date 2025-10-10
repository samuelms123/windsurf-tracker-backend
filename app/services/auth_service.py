import requests
from app.services import endpoints
from app import config

def get_access_token() -> str:
    payload:dict = {
    'client_id': config.STRAVA_CLIENT_ID,
    'client_secret': config.STRAVA_CLIENT_SECRET,
    'refresh_token': config.MY_REFRESH_TOKEN,
    'grant_type': "access_token",
    'f': 'json'
    }
    res = requests.post(endpoints.AUTH_ENDPOINT, data=payload, verify=False)
    access_token = res.json()['access_token']
    return access_token

def refresh_access_token(refresh_token: str) -> str:
    payload:dict = {
    'client_id': config.STRAVA_CLIENT_ID,
    'client_secret': config.STRAVA_CLIENT_SECRET,
    'refresh_token': refresh_token, ## config.MY_REFRESH_TOKEN for testing
    'grant_type': "refresh_token",
    'f': 'json'
    }
    res = requests.post(endpoints.AUTH_ENDPOINT, data=payload, verify=False)
    access_token = res.json()['access_token']
    return access_token