from functools import wraps

from flask import Blueprint, request

from app.extensions import mongoDB
from .pubnub_client import CLIENT

device_bp = Blueprint("devices", __name__)


# Decorator to validate certificate_string
def validate_certificate_string(func):
    @wraps(func)  # makes wrapper function "look" like the passed function
    def wrapper(*args, **kwargs):
        certificate_string = request.headers.get("certificate-string")
        sensor_id = request.headers.get("sensor-id")  # take from headers 'sensor-id'

        if not sensor_id or not certificate_string:
            return {"msg": "Missing credentials"}, 400

        sensor = mongoDB.db.sensor.find_one({"sensor_id": str(sensor_id)})
        if not sensor:
            return {"msg": "Sensor not found"}, 404

        if sensor.get("certificate_string") != str(certificate_string):
            return {"msg": "Unauthorized"}, 403

        return func(*args, **kwargs)

    return wrapper


@validate_certificate_string
def registerDevice():
    sensor_id = request.headers.get("sensor-id")  # take from headers 'sensor-id'

    channel_name = CLIENT.generate_chanel_name(sensor_id=sensor_id)
    sensor_token = CLIENT.grant_channel_access(channel_name, "telemetry-sensor")

    if not sensor_id:
        return {"msg": "Sensor_id not found"}, 404

    filter = {"sensor_id": sensor_id}
    result = mongoDB.db.sensor.update_one(filter, {"$set": {"channel_name": str(channel_name)}})

    if result.matched_count == 0:
        return {"msg": "Sensor not found"}, 404

    return {"channel": channel_name, "token": sensor_token}, 201


@validate_certificate_string
def refreshToken():
    sensor_id = request.headers.get("sensor-id")

    if not sensor_id:
        return {"msg": "Sensor_id not found"}, 404

    filter = {"sensor_id": sensor_id}

    channel_name = mongoDB.db.sensor.find_one(filter, {"channel_name": 1, "_id": 0})
    token = CLIENT.grant_channel_access(channel_name["channel_name"], "telemetry-sensor")

    return {"token": str(token)}, 200


@device_bp.route("/register", methods=["POST"])
def register_device():
    return registerDevice()


@device_bp.route("/refresh-token", methods=["POST"])
def refresh_token():
    return refreshToken()
