from .extensions import mongoDB
from datetime import datetime
from pymongo import DESCENDING

def store_per_hour():
    data = list(mongoDB.db.telemetry.find().sort("created_at", DESCENDING).limit(6))
    data.reverse()

    avg_temperature = round(sum(d.get("temperature", 0) for d in data) / len(data), 2)
    avg_humidity = int(sum(d.get("humidity", 0) for d in data) / len(data),2)
    avg_co2  = int(sum(d.get("co2", 0) for d in data) / len(data))
    avg_pm25 = int(sum(d.get("pm25", 0) for d in data) / len(data))
    
    mongoDB.db.telemetry_per_hour.insert_one({"avg_temperature": avg_temperature, 
                                              "avg_humidity" : avg_humidity,
                                              "avg_co2" : avg_co2,
                                              "avg_pm25" : avg_pm25,
                                              "updated_at": datetime.now() })
    
def store_per_day():
    data = list(mongoDB.db.telemetry_per_hour.find().sort("created_at", DESCENDING).limit(24))
    data.reverse()
    avg_temperature = round(sum(d.get("temperature", 0) for d in data) / len(data), 2)
    avg_humidity = int(sum(d.get("humidity", 0) for d in data) / len(data),2)
    avg_co2  = int(sum(d.get("co2", 0) for d in data) / len(data))
    avg_pm25 = int(sum(d.get("pm25", 0) for d in data) / len(data))
    
    mongoDB.db.telemetry_per_day.insert_one({"avg_temperature": avg_temperature, 
                                              "avg_humidity" : avg_humidity,
                                              "avg_co2" : avg_co2,
                                              "avg_pm25" : avg_pm25,
                                              "updated_at": datetime.now() })
    