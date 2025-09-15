from fastapi import FastAPI
from app.routes import strava_routes

app = FastAPI()

app.include_router(strava_routes.router)

@app.get("/")
def root():
    return {"msg": "Windsurf Tracker Backend is running!"}