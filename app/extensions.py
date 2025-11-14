from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

mongoDB = PyMongo()
jwt = JWTManager()
