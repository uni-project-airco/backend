from app.extensions import mongoDB
from .model import Telemetry
from pymongo import DESCENDING

def saveTelemetry(request):
    data = request.get_json()
    telemetry = Telemetry.from_mongo(data)

    telemetry.save()

    return {
        "msg": "Telemetry saved!",
    }, 200


def getTelemetryPerDay():
    return list(mongoDB.db.telemetry_per_hour.find().sort("created_at", DESCENDING).limit(24))[::-1]


def getTelemetryPerWeek():
    return list(mongoDB.db.telemetry_per_day.find().sort("created_at", DESCENDING).limit(7))[::-1]

def getHistoricalData():
    day = getTelemetryPerDay()
    week = getTelemetryPerWeek()

    if not day or not week:
        return {"msg" : "Unable to find historical data"}, 400
    
    return {"day" : day, "week" : week}, 200
