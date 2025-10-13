from fastapi import APIRouter
from app.services import auth_service
from app.schemas.auth import AuthMe, LoginRequest
from app.utils import hash
from app.config.database import user_collection
from bson import ObjectId
from app.utils.exceptions import UserNotFoundException
from app.schemas.user import individual_serial

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/access")
async def me(refresh_token: str):
    access_token = auth_service.get_access_token()
    return {"access_token": access_token}


@router.post("/me")
async def me(auth: AuthMe):
    access_token = auth_service.refresh_access_token(auth.refresh_token)
    return {"access_token": access_token}


@router.post("/login")
async def me(loginCredentials: LoginRequest):
    user = user_collection.find_one({"username": loginCredentials.username})
    
    if not user:
        print("User not found in db")
        raise UserNotFoundException()
    
    user_dict = individual_serial(user)
    
    if hash.verifyPassword(user_dict["password"], loginCredentials.password):
        user_dict.pop("password", None)
        return user_dict
    
    else:
        print("Unauthorized!")
        ## handle properly
    