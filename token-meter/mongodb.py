from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client["token_meter"]
collection = db["data"]

def insert_data(data: dict):
    data["timestamp"] = datetime.utcnow()
    result = collection.insert_one(data)
    print(f"inserted data to ID: {result.inserted_id}")
    return str(result.inserted_id)