from datetime import datetime, timezone

from bson import ObjectId


class TelemetryPerDay:
    def __init__(self, avg_temperature, avg_humidity, avg_co2, avg_pm25, updated_at=None, _id=None):
        self._id = str(_id) if _id else None
        self.avg_temperature = avg_temperature
        self.avg_humidity = avg_humidity
        self.avg_co2 = avg_co2
        self.avg_pm25 = avg_pm25
        self.updated_at = updated_at or datetime.now(timezone.utc)

    
    def to_dict(self):
        return {
            "avg_temperature" : self.avg_temperature,
            "avg_humidity" : self.avg_humidity,
            "avg_co2" : self.avg_co2,
            "avg_pm25" : self.avg_pm25,
            "updated_at" : self.updated_at
        }

    @staticmethod
    def from_mongo(data):
        return TelemetryPerDay(
            avg_temperature=data.get("avg_temperature"),
            avg_humidity=data.get("avg_humidity"),
            avg_co2=data.get("avg_co2"),
            avg_pm25=data.get("avg_pm25"),
            updated_at=data.get("updated_at"),
            _id = data.get("_id")
        )
    
    def get_by_id(db, telemetry_id):
        data = db.telemetry_per_day.find_one({"_id":ObjectId(telemetry_id)})
        return TelemetryPerDay.from_mongo(data) if data else None
    
    def get_by_date(db,date_time):
        data = db.telemetry_per_day.find_one({"updated_at":date_time})
        return TelemetryPerDay.from_mongo(data) if data else None
