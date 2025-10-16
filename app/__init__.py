from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)

    app.config["MONGO_URI"] = "mongodb://localhost:27017"
    mongo.init_app(app)

    from app.users.routes import users_bp

    app.register_blueprint(users_bp, url_prefix="/users")

    return app