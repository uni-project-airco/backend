from datetime import datetime
from bson import ObjectId
from app import mongo

class Notification:
    def __init__(self, metric, threshold, is_enabled, _id = None):
        self.metric = metric
        self.threshold = threshold
        self.is_enabled = is_enabled
        self._id = _id

    def to_dict(self):
        return {
            "metric" : self.metric,
            "threshold" : self.threshold,
            "is_enabled" : self.is_enabled,
        }

    @staticmethod
    def from_mongo(data):
        return Notification(
            metric=data.get("metric"),
            threshold = data.get("threshold"),
            is_enabled = data.get("is_enabled"),
            _id = data.get("_id")
        )
    
    @staticmethod
    def get_by_metric(metric):
        data = mongo.db.notifications.find_one({"metric":metric})
        return Notification.from_mongo(data) if data else None
    
    @staticmethod
    def get_by_metric(notification_id):
        data = mongo.db.notifications.find_one({"_id":ObjectId(notification_id)})
        return Notification.from_mongo(data) if data else None