from pymongo import MongoClient
from app.config import dotenv

client = MongoClient(dotenv.MONGO_URI)
db = client.windsurt_app_db

metadata = db["metadata"]
activity_collection = db["activity_collection"]
activity_summary = db["activity_summary"]
