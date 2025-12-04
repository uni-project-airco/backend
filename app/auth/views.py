from ..users.model import User
from app.extensions import mongoDB
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from ..devices.pubnub_client import CLIENT


def generateAccessToken(identity):
    return create_access_token(identity)


def generateRefreshToken(identity):
    return create_refresh_token(identity)


def registerUser(request):
    data = request.get_json()

    user = User.from_mongo(data)

    if mongoDB.db.users.find_one({"username": user.username}):
        return {"msg": "You already have an account. Try Login"}

    user.save()

    access_token = generateAccessToken(str(user.id))
    refresh_token = generateRefreshToken(str(user.id))

    return {
        "msg": "User successfully registered and logged in",
        "access_token": access_token,
        "refresh_token": refresh_token,
    }, 200


def loginUser(request):
    data = request.get_json()

    password = data.get("password")
    username = data.get("username")

    user = mongoDB.db.users.find_one({"username": username})
    print(user)

    if not user or not check_password_hash(user.get("password"), password):
        return {"msg": "Bad credentials"}, 403

    access_token = generateAccessToken(str(user.get("_id")))
    refresh_token = generateRefreshToken(str(user.get("_id")))
    sensor_id = request.headers.get("sensor-id")

    channel_name = CLIENT.generate_chanel_name(sensor_id=sensor_id)
    sensor_token = CLIENT.grant_channel_access(channel_name, "telemetry-sensor")

    return {"access_token": access_token, "refresh_token": refresh_token, "sensor_token" : sensor_token}, 200


def refreshToken():
    user_id = get_jwt_identity()
    access_token = create_access_token(str(user_id))
    return {"access_token": access_token}, 200
