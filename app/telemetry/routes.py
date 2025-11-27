from flask import request, Blueprint

from .views import *

telemetry_bp = Blueprint("telemetry", __name__)


# TODO add decorator, validate device by certificate_string
@telemetry_bp.route("/save_telemetry", methods=["POST"])
def save_telemetry():
    if not request.is_json:
        return {"msg": "No JSON provided"}, 400
    return saveTelemetry(request)


@telemetry_bp.route("/get_telemetry_per_day", methods=["GET"])
def get_telemetry_per_day():
    return getTelemetryPerDay()


@telemetry_bp.route("/get_telemetry_per_week", methods=["GET"])
def get_telemetry_per_day():
    return getTelemetryPerWeek()
