from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/vpn", tags=["Health"])
async def vpn_ping():
    return {"status": "healthy"}