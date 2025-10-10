from fastapi import FastAPI
from app.routes import strava_routes, auth_routes, user_routes

app = FastAPI()

app.include_router(strava_routes.router)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)

@app.get("/")
def root():
    return {"msg": "Windsurf Tracker Backend is running!"}

