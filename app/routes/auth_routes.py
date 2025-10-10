from fastapi import APIRouter
from app.services import auth_service
from app.schemas.auth import AuthMe

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/access")
async def me(refresh_token: str):
    access_token = auth_service.get_access_token()
    return {"access_token": access_token}


@router.post("/me")
async def me(auth: AuthMe):
    access_token = auth_service.refresh_access_token(auth.refresh_token)
    return {"access_token": access_token}