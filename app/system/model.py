from bson import ObjectId

class System:
    def __init__(self, name, description, users=None, _id=None):
        self._id = str(_id) if _id else None
        self.name = name
        self.description = description

    def to_dict(self):
        return {
            "name": self.name,
            "description":self.description
        }