from pydantic import BaseModel, Field
from datetime import datetime
    
class SpeedZones(BaseModel):
    idle: int
    low: int
    planing_entry: int
    planing: int
    blasting: int

class Location(BaseModel):
    street: str | None
    neighborhood: str | None
    suburb: str | None
    city_district: str | None
    city: str | None
    municipality: str | None
    region: str | None
    area: str | None
    postal_code: str | None
    country: str | None
    
class Activity(BaseModel):
    id: str = Field(..., description="Strava activity ID")
    date: datetime = Field(..., description="Activity date")
    start_location: Location = Field(..., description="Activity start location")
    elapsed_time: int = Field(..., description="Activity duration (s)")

    average_speed: float = Field(..., description="Average speed (m/s)")
    max_speed: float = Field(..., description="Max instantaneous speed (m/s)")
    max_speed_avg_5_s: float = Field(..., description="Max 5-second average speed (m/s)")
    max_speed_avg_10_s: float = Field(..., description="Max 10-second average speed (m/s)")
    fastest_100: int | None = Field(..., description="Fastest 100m time (s)")
    fastest_500: int | None = Field(..., description="Fastest 500m time (s)")
    fastest_1000: int | None = Field(..., description="Fastest 1000m time (s)")
    total_distance: float = Field(..., description="Total distance (m)")
    speed_zones: SpeedZones = Field(..., description="Time spent in named speed zones (s)")
    
    
def serialize_activity(activity):
    if '_id' in activity:
        activity['id'] = str(activity['_id'])
        del activity['_id']
    return activity