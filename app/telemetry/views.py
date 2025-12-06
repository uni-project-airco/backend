from pymongo import DESCENDING

from app.extensions import mongoDB
from .model import Telemetry
from pymongo import DESCENDING
from datetime import datetime


def saveTelemetry(request):
    data = request.get_json()
    sensor_id = request.headers.get("sensor-id")
    telemetry = Telemetry.from_mongo(data, sensor_id)

    telemetry.save()

    return {
        "msg": "Telemetry saved!",
    }, 200


def serialize_doc(doc):
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.isoformat()

        if isinstance(value, dict) and "$date" in value:
            doc[key] = value["$date"]

    return doc

def getTelemetryPerDay():
    data = list(mongoDB.db.telemetry_per_hour.find({}, {"_id": 0}).sort("updated_at", DESCENDING).limit(24))[::-1]
    data = data[::4]
    return [serialize_doc(d) for d in data]

def getTelemetryPerWeek():
    data = list(mongoDB.db.telemetry_per_day.find({}, {"_id": 0}).sort("updated_at", DESCENDING).limit(7))[::-1]
    return [serialize_doc(d) for d in data]


def getHistoricalData():
    day = getTelemetryPerDay()
    week = getTelemetryPerWeek()

    if not day or not week:
        return {"msg": "Unable to find historical data"}, 400

    return {"day": day, "week": week}, 200
