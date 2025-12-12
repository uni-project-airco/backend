import os
import uuid
from datetime import timedelta
from logging.config import dictConfig
from urllib.parse import quote_plus

from dotenv import load_dotenv, find_dotenv
from flask import Flask

# Blueprints
from app.auth.routes import auth_bp
from app.devices.routes import device_bp
from app.extensions import mongoDB, jwt, scheduler
from app.jobs import store_per_hour, store_per_day
from app.system.routes import system_bp
from app.telemetry.routes import telemetry_bp
from app.users.routes import users_bp

def create_app():
    load_dotenv(find_dotenv())

    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                }
            },
            "root": {"level": "INFO", "handlers": ["wsgi"]},
        }
    )

    app = Flask(__name__)

    # --- PROD ---
    db_user = os.getenv("MONGO_USER")
    db_password = quote_plus(os.getenv("MONGO_PASSWORD"))
    db_name = os.getenv("MONGO_DB_NAME")
    cluster_name = os.getenv("MONGO_CLUSTER_NAME")
    app.config["MONGO_URI"] = (
        f"mongodb+srv://{db_user}:{db_password}@{cluster_name}.mongodb.net/{db_name}?retryWrites=true&w=majority"
    )
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60)
    mongoDB.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(system_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(telemetry_bp, url_prefix="/telemetry")
    app.register_blueprint(device_bp, url_prefix="/sensor")

    with app.app_context():
        if not scheduler.get_jobs():
            scheduler.add_job(func=store_per_hour, trigger='cron', minute=0, id=str(uuid.uuid4()))
            scheduler.add_job(func=store_per_day, trigger='cron', hour=0, minute=0, id=str(uuid.uuid4()))
            if not scheduler.running:
                scheduler.start()

    return app
