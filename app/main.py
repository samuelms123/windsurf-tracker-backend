from datetime import datetime
from pathlib import Path
import pandas as pd

from services import fetch_service, strava_auth


def main():
    token: str = strava_service.get_access_token()
    result = fetch_service.get_activity_data(token)
    print(result)

if __name__ == '__main__':
    main()