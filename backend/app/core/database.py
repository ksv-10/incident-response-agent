import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "incident_response_agent"
)

client = None
db = None


def connect_to_mongodb():
    global client, db

    if not MONGODB_URI:
        raise ValueError("MONGODB_URI missing from .env")

    client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=10000
    )

    client.admin.command("ping")
    db = client[DATABASE_NAME]

    print("MongoDB Atlas connected successfully!")

    return db