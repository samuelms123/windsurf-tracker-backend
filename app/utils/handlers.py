from app.utils import exceptions
from fastapi.responses import JSONResponse
from fastapi import Request

def add_exception_handlers(app):
     
    @app.exception_handler(exceptions.InvalidTokenError)
    async def invalid_token_handler(request: Request, exception: exceptions.InvalidTokenError):
        return JSONResponse(
            status_code=exception.status_code,
            content={"error": exception.message}
        )
    
    @app.exception_handler(exceptions.InvalidAPIKeyError)
    async def invalid_apikey_handler(request: Request, exception: exceptions.InvalidAPIKeyError):
        return JSONResponse(
            status_code=exception.status_code,
            content={"error": exception.message}
        )
        