from fastapi import FastAPI
from app.routes import master_router
from fastapi.middleware.cors import CORSMiddleware

from app.utils.handlers import add_exception_handlers

app = FastAPI()
origins = [
    "http://localhost:5173",   
    "http://127.0.0.1:5173",
    "https://windsurf-tracker-frontend.vercel.app",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)

app.include_router(master_router, prefix="/api/v1")

add_exception_handlers(app)