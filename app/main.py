from fastapi import FastAPI
from app.routes import strava_routes, auth_routes, user_routes

from app.utils.handlers import add_exception_handlers

app = FastAPI()

app.include_router(strava_routes.router)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)

add_exception_handlers(app)