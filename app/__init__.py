import os
from datetime import timedelta
from logging.config import dictConfig

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

mongo = PyMongo()
jwt = JWTManager()


def create_app():
    load_dotenv(find_dotenv())

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    app = Flask(__name__)

    app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60)
    mongo.init_app(app)
    jwt.init_app(app)

    # Blueprints
    from app.users.routes import users_bp
    from app.system.routes import system_bp
    from app.auth.routes import auth_bp

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(system_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app