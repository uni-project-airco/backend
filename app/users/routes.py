from flask import Blueprint, request
from .views import *
from flask_jwt_extended import jwt_required

users_bp = Blueprint("users", __name__)

@users_bp.route("/changeUsername", methods=["PATCH"])
@jwt_required()
def change_username():
    return changeUsername(request)

@users_bp.route("/changeEmail", methods=["PATCH"])
@jwt_required()
def change_email():
    return changeEmail(request)

@users_bp.route("/changePassword", methods=["PATCH"])
@jwt_required()
def change_password():
    return changePassword(request)