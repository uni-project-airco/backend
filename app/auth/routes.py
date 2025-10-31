from flask import Blueprint, request
from app import mongo
from flask_jwt_extended import jwt_required

from .views import *

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return {"msg" : "No JSON provided"}, 400
    return registerUser(request)

@auth_bp.route("login", methods=["POST"])
def login():
    if not request.is_json:
        return {"msg" : "No JSON provided"}, 400
    return loginUser(request)

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    return refreshToken()

@auth_bp.route("/verify", methods=["GET"])
@jwt_required()
def verify():
    return {"msg" : "Valid"}, 200