from app.utils import exceptions
from fastapi.responses import JSONResponse
from fastapi import Request

def add_exception_handlers(app):
    
    @app.exception_handler(exceptions.LoginCredentialException)
    async def user_not_found_handler(request: Request, exception: exceptions.LoginCredentialException):
        return JSONResponse(
            status_code=exception.status_code,
            content={"error": exception.message}
        )
        
    
    ## Add more in same way.