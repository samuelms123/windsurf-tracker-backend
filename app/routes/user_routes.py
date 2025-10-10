from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

### User/Database related routes