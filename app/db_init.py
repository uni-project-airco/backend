from app import mongo_dev
from app import  mongo_prod
from pymongo import ASCENDING


def init_db():
    for mongo in [mongo_dev, mongo_prod]:
        db = mongo.db

        if "users" not in db.list_collection_names():
            db.create_collection("users")
        db.users.create_index([("email", ASCENDING)], unique=True)
        db.users.create_index([("username", ASCENDING)], unique=True)

        if "auth" not in db.list_collection_names():
            db.create_collection("auth")
        db.auth.create_index([("email", ASCENDING)], unique=True)
        db.auth.create_index([("username", ASCENDING)], unique=True)

        if "system" not in db.list_collection_names():
            db.create_collection("system")
        db.system.create_index([("name", ASCENDING)], unique=True)

        if "notifications" not in db.list_collection_names():
            db.create_collection("notifications")
        db.notifications.create_index([("id", ASCENDING)], unique=True)

        if "telemetry" not in db.list_collection_names():
            db.create_collection("telemetry")
        db.telemetry.create_index([("id", ASCENDING)], unique=True)
        db.telemetry.create_index([("created_at", ASCENDING)])



