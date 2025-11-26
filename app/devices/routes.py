from flask import Blueprint, request

import pubnub_client

device_bp = Blueprint("devices", __name__)


@device_bp.route("/register", methods=["POST"])
def register_device():
    body = request.json
    sensor_id = body.get("sensor_id", None)
    certificate_string = body.get("certificate_string", None)

    if sensor_id is None or certificate_string is None:
        return {"msg": "Invalid request"}, 400

    # TODO add validation if access_token does not match with saved in db return 403, maybe create decorator

    channel_name = pubnub_client.CLIENT.generate_chanel_name(sensor_id=sensor_id)
    sensor_token = pubnub_client.CLIENT.grant_channel_access(channel_name, "telemetry-sensor")

    # TODO update 'channel_name' in device record
    return {"channel": channel_name, "token": sensor_token}, 201
