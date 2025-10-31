from datetime import datetime
from bson import ObjectId
from app import mongo 
from werkzeug.security import generate_password_hash, check_password_hash

class AuthUser:
    def __init__(self, username, email, password, created_at=None, _id=None):
        self._id = str(_id) if _id else None
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at or datetime.now()
        
    def to_dict(self):
        return {
            "username" : self.username,
            "email" : self.email,
            "password" : self.password,
            "created_at" : self.created_at,
        }
    
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)
    
    @staticmethod
    def from_mongo(data):
        return AuthUser(
            username = data.get("username"),
            email = data.get("email"),
            password = data.get("password"),
            created_at = data.get("created_at"),
            _id = data.get("_id")
        )
    
    @staticmethod
    def find_by_email(email):
        data = mongo.db.users.find_one({"email": email})
        return AuthUser.from_mongo(data) if data else None
    
    def save(self):
        if self.password and not self.password.startswith("pbkdf2:sha256:"):
            self.password = self.hash_password(self.password)

        user = mongo.db.users.insert_one(self.to_dict())
        self._id = str(user.inserted_id)
        return self._id