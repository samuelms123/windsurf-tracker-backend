from fastapi import APIRouter
from app.services import auth_service
from app.schemas.auth import AuthMe, LoginRequest
from app.utils import security
from app.config.database import user_collection
from app.utils.exceptions import LoginCredentialError
from app.schemas.user import individual_serial

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/access")
async def access_token(refresh_token: str):
    access_token = auth_service.get_access_token()
    return access_token


@router.post("/me")
async def auth_me(auth: AuthMe):
    access_token = auth_service.refresh_access_token(auth.refresh_token)
    return access_token


@router.post("/login")
async def login(login_credentials: LoginRequest):
    user = user_collection.find_one({"username": login_credentials.username})
    
    if not user:
        raise LoginCredentialError()
    
    user_dict = individual_serial(user)
    
    if security.verify_password(user_dict["password"], login_credentials.password):
        user_dict.pop("password", None)
        return user_dict
    
    else:
        raise LoginCredentialError()
    