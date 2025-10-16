from bson import ObjectId
from app import mongo

class System:
    def __init__(self, name, users=None, _id=None):
        self._id = str(_id) if _id else None
        self.name = name

    def to_dict(self):
        return {
            "name": self.name,
        }