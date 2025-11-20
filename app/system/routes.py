from flask import Blueprint

system_bp = Blueprint("system", __name__)


@system_bp.route("/")
def index():
    return "Home!"
