from ..users.model import User
from app import mongo
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity

def generateAccessToken(identity):
    return create_access_token(identity)

def generateRefreshToken(identity):
    return create_refresh_token(identity)

def registerUser(request):
    data = request.get_json()

    user = User.from_mongo(data)

    if mongo.db.users.find_one({"username" : user.username}):
        return {"msg" : "You already have an account. Try Login"}
    
    userId = user.save()

    access_token = generateAccessToken(str(user.get("id")))
    refresh_token = generateRefreshToken(str(user.get("id")))
    
    return {"msg" : "User successfully registered and logged in", "access_token" : access_token, "refresh_token" : refresh_token}, 200

    
def loginUser(request):
    data = request.get_json()

    password = data.get("password")
    username = data.get("username")

    user = mongo.db.users.find_one({"username" : username})

    if not user or not check_password_hash(user.get("password"), password):
        return {"msg" : "Bad credentials"}, 403
    
    access_token = generateAccessToken(str(user.get("id")))
    refresh_token = generateRefreshToken(str(user.get("id")))

    return {"access_token" : access_token, "refresh_token" : refresh_token}, 200

def refreshToken():
    user_id = get_jwt_identity()
    access_token = create_access_token(str(user_id))
    return {"access_token" : access_token}, 200


def verifyToken():
    return {"msg": "Token is valid"}, 200