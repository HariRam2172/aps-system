import os

from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError(
        "MONGO_URI is not set. Add it to your environment before starting the app."
    )

client = MongoClient(MONGO_URI)

# Database name
db = client["aps_db"]

# Collections
tasks_collection = db["tasks"]
notes_collection = db["notes"]
events_collection = db["events"]
