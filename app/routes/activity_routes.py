from fastapi import APIRouter
from app.models import activity_models

router = APIRouter(prefix="/activities", tags=["Activities"])

@router.get("")
async def get_synced_activities(username: str):
    return await activity_models.get_analyzed_activities(username)