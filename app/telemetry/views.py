from .model import Telemetry
from app.extensions import mongoDB

def saveTelemetry(request):
    data = request.get_json()
    telemetry = Telemetry.from_mongo(data)
    
    telemetry.save()

    return {
        "msg": "Telemetry saved!",
    }, 200

def getTelemetryPerDay():
    return mongoDB.db.telemetry_per_hour.find().sort("created_at", DESCENDING).limit(24).reverse()

def getTelemetryPerWeek():
    return mongoDB.db.telemetry_per_day.find().sort("created_at", DESCENDING).limit(7).reverse()
    