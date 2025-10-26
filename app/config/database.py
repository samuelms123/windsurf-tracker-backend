from pymongo import MongoClient, ASCENDING
from app.config import dotenv

client = MongoClient(dotenv.MONGO_URI)
db = client.windsurt_app_db
user_collection = db["user_collection"]
activity_collection = db["activity_collection"]

user_collection.create_index([("username", ASCENDING)], unique=True)