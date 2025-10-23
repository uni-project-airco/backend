from flask import Blueprint
from app import mongo

system_bp = Blueprint("system", __name__)

@system_bp.route("/")
def index():
    return "Home!"