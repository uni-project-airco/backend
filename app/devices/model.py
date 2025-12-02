import uuid
from datetime import datetime

class Device:
    def __init__(self, sensor_id, certificate_string, created_at=None, updated_at = None, channel_name=None):
        self.sensor_id = sensor_id or str(uuid.uuid4())
        self.certificate_string = str(certificate_string)
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.channel_name = str(channel_name) if channel_name else None

    def to_dict(self):
        return {
            "sensor_id" : self.sensor_id,
            "certificate_string": self.certificate_string,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "channel_name": self.channel_name
        }

    @staticmethod
    def from_mongo(data):
        return Device(
            sensor_id=data.get("sensor_id"),
            certificate_string=data.get("certificate_string"),
            channel_name=data.get("channel_name"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
    
    def save(self, db):
        sensor = db.sensor.insert_one(self.to_dict())
        return self.sensor_id

# fields: sensor_id: uuid4, created_at, updated_at: |None, channel_name: str|None, certificate_string: str
