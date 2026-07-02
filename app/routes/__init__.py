from fastapi import APIRouter
from .strava_routes import router as strava_router
from .activity_routes import router as activity_router

master_router = APIRouter()

# Group
master_router.include_router(strava_router)
master_router.include_router(activity_router)