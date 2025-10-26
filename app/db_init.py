from app import mongo_dev, create_app
from app import  mongo_prod
from pymongo import ASCENDING

app = create_app()

def init_db_for(db):
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

    if "telemetry_per_day" not in db.list_collection_names():
        db.create_collection("telemetry_per_day")
    db.telemetry.create_index([("id", ASCENDING)], unique=True)
    db.telemetry.create_index([("updated_at", ASCENDING)])

    if "telemetry_per_hour" not in db.list_collection_names():
        db.create_collection("telemetry_per_hour")
    db.telemetry.create_index([("id", ASCENDING)], unique=True)
    db.telemetry.create_index([("updated_at", ASCENDING)])

    if "telemetry" not in db.list_collection_names():
        db.create_collection("telemetry")
    db.telemetry.create_index([("id", ASCENDING)], unique=True)
    db.telemetry.create_index([("created_at", ASCENDING)])



def init_db():
    with app.app_context():
        init_db_for(mongo_dev.db)
        init_db_for(mongo_prod.db)

if __name__ == "__main__":
    init_db()
