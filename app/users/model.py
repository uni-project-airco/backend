from datetime import datetime
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo

class User:
    def __init__(self, system_id, username, email, password, notifications=None, is_admin=False, created_at=None, _id=None):
        self._id = str(_id) if _id else None
        self.system_id = str(system_id) if system_id else None
        self.username = username
        self.email = email
        self.password = password
        self.notifications = notifications or []
        self.is_admin = is_admin if is_admin else False
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            "system_id" : self.system_id,
            "username" : self.username,
            "email" : self.email,
            "password" : self.password,
            "notifications" : [ObjectId(a) for a in self.notifications],
            "is_admin" : self.is_admin,
            "created_at" : self.created_at 
        }
    
    @staticmethod
    def from_mongo(data):
        return User(
            system_id = data.get("system_id"),
            username=data.get("username"),
            email = data.get("email"),
            password = data.get("password"),
            notifications = data.get("notifications"),
            is_admin = data.get("is_admin"),
            created_at = data.get("created_at"),
            _id = data.get("_id")
        )
    
    @staticmethod
    def get_by_id(user_id):
        user_data = mongo.db.users.find_one({"_id":ObjectId(user_id)})
        return User.from_mongo(user_data) if user_data else None
    
    @staticmethod
    def get_by_email(user_email):
        user_data = mongo.db.users.find_one({"email":user_email})
        return User.from_mongo(user_data) if user_data else None
    
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)
    
    def save(self):
        if self.password and not self.password.startswith("pbkdf2:sha256:"):
            self.password = self.hash_password(self.password)

        user = mongo.db.users.insert_one(self.to_dict())
        self._id = str(user.inserted_id)
        return self._id
