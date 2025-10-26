from fastapi import APIRouter, Security
from app.services import auth_service
from app.schemas.auth import AuthMe, LoginRequest
from app.utils import security
from app.config.database import user_collection
from app.utils.exceptions import LoginCredentialError, InvalidTokenError
from app.schemas.user import individual_serial
from app.utils.security import decrypt_token, create_jwt_token_for_database
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.user_models import get_user



router = APIRouter(prefix="/auth", tags=["Authentication"])
bearer_scheme = HTTPBearer()

@router.post("/me")
async def refresh_jwt(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    token = credentials.credentials
    payload = security.decode_jwt_token(token, verify_exp=False)
    username = payload.get("username")
    if not username:
        raise InvalidTokenError
    
    user = await get_user(username)
    user_dict = individual_serial(user)
    user_dict.pop("password", None)
    user_dict.pop("refresh_token", None)
    user_dict.pop("access_token", None)
    token = create_jwt_token_for_database(user_dict)
    
    return {"user": user_dict,
            "token": token
            }
    


@router.post("/login")
async def login(login_credentials: LoginRequest):
    user = user_collection.find_one({"username": login_credentials.username})
    
    if not user:
        raise LoginCredentialError()
    
    user_dict = individual_serial(user)
    
    if security.verify_password(user_dict["password"], login_credentials.password):
        user_dict.pop("password", None)
        user_dict.pop("refresh_token", None)
        user_dict.pop("access_token", None)
        
        token = create_jwt_token_for_database(user_dict)
        return {"user": user_dict,
                "token": token
                }
    
    else:
        raise LoginCredentialError()
    