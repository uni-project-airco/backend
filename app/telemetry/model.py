from datetime import datetime, timezone

from bson import ObjectId

from app.extensions import mongoDB


class Telemetry:
    def __init__(self, temperature, humidity, co2, pm25, sensor_id, created_at=None, _id=None):
        self._id = str(_id) if _id else None
        self.sensor_id = sensor_id
        self.temperature = temperature
        self.humidity = humidity
        self.co2 = co2
        self.pm25 = pm25
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "co2": self.co2,
            "pm25": self.pm25,
            "created_at": self.created_at,
            "sensor_id": self.sensor_id
        }

    @staticmethod
    def from_mongo(data, sensor_id):
        return Telemetry(
            temperature=data.get("temperature"),
            humidity=data.get("humidity"),
            co2=data.get("co2"),
            pm25=data.get("pm25"),
            sensor_id=sensor_id
        )

    def get_by_id(self, telemetry_id):
        data = mongoDB.db.telemetry.find_one({"_id": ObjectId(telemetry_id)})
        return Telemetry.from_mongo(data) if data else None

    def get_by_date(self, date_time):
        data = mongoDB.db.telemetry.find_one({"created_at": date_time})
        return Telemetry.from_mongo(data) if data else None

    def save(self):
        telemetry = mongoDB.db.telemetry.insert_one(self.to_dict())
        self._id = str(telemetry.inserted_id)
        return self._id
