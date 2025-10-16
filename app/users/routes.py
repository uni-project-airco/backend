from flask import Blueprint
from app import mongo

users_bp = Blueprint("users", __name__)

@users_bp.route("/")
def index():
    return "Hello World"