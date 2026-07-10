from fastapi import APIRouter
from app.models import activity_models, summary_models
from app.utils.exceptions import EmptySummaryError
from app.schemas.activities import Activity, Summary

router = APIRouter(prefix="/activities", tags=["Activities"])

@router.get("", response_model=list[Activity])
async def get_synced_activities():
    
    return activity_models.get_analyzed_activities()


@router.get("/summary", response_model=Summary)
async def get_activity_summary():
    summary = summary_models.get_summary()

    if summary is None:
        raise EmptySummaryError
    
    return summary
    
