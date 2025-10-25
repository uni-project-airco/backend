from urllib.parse import quote_plus

from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
mongo_dev = PyMongo()
mongo_prod = PyMongo()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    # --- DEV ---

    user_dev = os.getenv("MONGO_USER_DEV")
    password_dev = os.getenv("MONGO_PASSWORD_DEV")
    db_name_dev = os.getenv("MONGO_DB_DEV")
    cluster_dev = os.getenv("MONGO_CLUSTER_DEV")
    password_encoded_dev = quote_plus(password_dev)
    app.config["MONGO_URI_DEV"] = f"mongodb+srv://{user_dev}:{password_encoded_dev}@{cluster_dev}.mongodb.net/{db_name_dev}?retryWrites=true&w=majority"

    mongo_dev.init_app(app, uri=app.config["MONGO_URI_DEV"])
    # --- PROD ---
    user_prod = os.getenv("MONGO_USER_PROD")
    password_prod = quote_plus(os.getenv("MONGO_PASSWORD_PROD"))
    db_prod = os.getenv("MONGO_DB_PROD")
    cluster_prod = os.getenv("MONGO_CLUSTER_PROD")
    app.config["MONGO_URI_PROD"] = f"mongodb+srv://{user_prod}:{password_prod}@{cluster_prod}.mongodb.net/{db_prod}?retryWrites=true&w=majority"
    mongo_prod.init_app(app, uri=app.config["MONGO_URI_PROD"])



    from app.users.routes import users_bp

    app.register_blueprint(users_bp, url_prefix="/users")

    return app