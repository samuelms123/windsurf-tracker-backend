from pydantic import BaseModel, Field
from datetime import datetime
    
class SpeedZones(BaseModel):
    idle: int
    low: int
    planing_entry: int
    planing: int
    blasting: int
    
class Activity(BaseModel):
    max_speed_avg_5_s: float = Field(..., description="Max 5-second average speed (m/s)")
    max_speed_avg_10_s: float = Field(..., description="Max 10-second average speed (m/s)")
    speed_zones: SpeedZones = Field(..., description="Time spent in names speed zones (s)")
    fastest_100: int = Field(..., description="Fastest 100m time (s)")
    fastest_500: int = Field(..., description="Fastest 500m time (s)")
    fastest_1000: int = Field(..., description="Fastest 1000m time (s)")
    date: datetime
    elapsed_time: int = Field(..., description="Total activity duration (s)")
    average_speed: float = Field(..., description="Average speed (m/s)")
    max_speed: float = Field(..., description="Max instantaneous speed (m/s)")
    total_distance: float = Field(..., description="Total distance (m)")
    
    
def serialize_activity(activity):
    activity['id'] = str(activity['_id'])
    activity['user_id'] = str(activity['user_id'])
    del activity['_id']
    return activity