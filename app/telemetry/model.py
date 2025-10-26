from datetime import datetime, timezone
from bson import ObjectId

class Telemetry:
    def __init__(self, temperature, humidity, co2, pm25, created_at=None, _id=None):
        self._id = str(_id) if _id else None
        self.temperature = temperature
        self.humidity = humidity
        self.co2 = co2
        self.pm25 = pm25
        self.created_at = created_at or datetime.now(timezone.utc)

    
    def to_dict(self):
        return {
            "temperature" : self.temperature,
            "humidity" : self.humidity,
            "co2" : self.co2,
            "pm25" : self.pm25,
            "created_at" : self.created_at
        }

    @staticmethod
    def from_mongo(data):
        return Telemetry(
            temperature=data.get("temperature"),
            humidity=data.get("humidity"),
            co2=data.get("co2"),
            pm25=data.get("pm25"),
            created_at=data.get("created_at"),
            _id = data.get("_id")
        )
    
    def get_by_id(db,telemetry_id):
        data = db.telemetry.find_one({"_id":ObjectId(telemetry_id)})
        return Telemetry.from_mongo(data) if data else None
    
    def get_by_date(db,date_time):
        data = db.telemetry.find_one({"created_at":date_time})
        return Telemetry.from_mongo(data) if data else None
