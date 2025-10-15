from app.utils import exceptions
from fastapi.responses import JSONResponse
from fastapi import Request

def add_exception_handlers(app):
    
    @app.exception_handler(exceptions.LoginCredentialError)
    async def user_not_found_handler(request: Request, exception: exceptions.LoginCredentialError):
        return JSONResponse(
            status_code=exception.status_code,
            content={"error": exception.message}
        )
        
    @app.exception_handler(exceptions.InvalidTokenError)
    async def invalid_token_handler(request: Request, exception: exceptions.InvalidTokenError):
        return JSONResponse(
            status_code=exception.status_code,
            content={"error": exception.message}
        )