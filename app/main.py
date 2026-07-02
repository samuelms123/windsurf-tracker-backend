from fastapi import FastAPI
from app.routes import master_router

from app.utils.handlers import add_exception_handlers

app = FastAPI()

app.include_router(master_router, prefix="/api/v1")

add_exception_handlers(app)