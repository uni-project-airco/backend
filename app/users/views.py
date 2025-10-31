from flask_jwt_extended import get_jwt_identity
from ..users.model import User
from app import mongo

def changeUsername(request):
    user_id = get_jwt_identity()

    if not user_id:
        return {"msg" : "user_id is missing"}, 400
        
    user = User.get_by_id(user_id)
    username = request.json.get("username")

    if not username:
        return {"msg" : "username missing"}, 400
    
    mongo.db.users.update_one({"username" : user.username}, { "$set": { "username": username } })
    
    return {"msg" : "username is successfully changed"}, 200

def changeEmail(request):
    user_id = get_jwt_identity()

    if not user_id:
        return {"msg" : "user_id is missing"}, 400
    
    user = User.get_by_id(user_id)
    email = request.json.get("email")

    if not email:
        return {"msg" : "email missing"}, 400
    
    mongo.db.users.update_one({"email" : user.email}, { "$set": { "email": email } })
    
    return {"msg" : "email is successfully changed"}, 200

def changePassword(request):
    user_id = get_jwt_identity()

    if not user_id:
        return {"msg" : "user_id is missing"}, 400
    
    user = User.get_by_id(user_id)
    oldPassword = request.json.get("oldPassword")
    newPassword = request.json.get("newPassword")

    if not oldPassword or not newPassword:
        return {"msg" : "old password or new password missing"}, 400
    
    if not user.verify_password(user.password, oldPassword):
        return {"msg":"wrong password"}, 403
    
    mongo.db.users.update_one({"password" : user.password}, { "$set": { "password": user.hash_password(newPassword) } })
    
    return {"msg" : "password is successfully changed"}, 200