from pymongo import MongoClient
from app.config import dotenv

client = MongoClient(dotenv.MONGO_URI)
db = client.windsurt_app_db
user_collection = db["user_collection"]