from flask import Blueprint, request

import pubnub_client

device_bp = Blueprint("devices", __name__) # TODO add to app


@device_bp.route("/register", methods=["POST"])
def register_device():
    body = request.json
    sensor_id = body.get("sensor_id", None) # take from headers 'sensor-id'
    # certificate_string = body.get("certificate_string", None) # take from headers 'certificate-string'


    # TODO add validation if certificate_string does not match with saved in db return 403, create decorator

    channel_name = pubnub_client.CLIENT.generate_chanel_name(sensor_id=sensor_id)
    sensor_token = pubnub_client.CLIENT.grant_channel_access(channel_name, "telemetry-sensor")

    # TODO update 'channel_name' in device record
    return {"channel": channel_name, "token": sensor_token}, 201
