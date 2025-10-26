from datetime import datetime, timezone
from app import create_app, mongo_dev
from app.auth.model import AuthUser
from app.system.model import System
from app.telemetry.model import Telemetry
from app.telemetry.model_day import TelemetryPerDay
from app.telemetry.model_hour import TelemetryPerHour
from app.users.model import User
from app.notifications.model import Notification

app = create_app()

def seed_users(db):
    if db.users.count_documents({}) == 0:
        admin_user = User(
            username="admin",
            email="admin@safeair.dev",
            password="hashed_admin_password",
            is_admin=True,
            system_id=0
        )

        tester_user = User(
            username="tester",
            email="tester@safeair.dev",
            password="hashed_tester_password",
            is_admin=False,
            system_id=0
        )

        db.users.insert_many([admin_user.to_dict(), tester_user.to_dict()])
        print("\N{GRINNING FACE} Users created")
    else:
        print("\N{SMILING FACE WITH OPEN MOUTH AND COLD SWEAT} Users already exist")


def seed_notifications(db):
    if db.notifications.count_documents({}) == 0:
        notification = Notification(
            metric="metric",
            threshold=20.0,
            is_enabled=True
        )
        db.notifications.insert_one(notification.to_dict())
        print("\N{GRINNING FACE} Notification created")
    else:
        print("\N{SMILING FACE WITH OPEN MOUTH AND COLD SWEAT} Notification already exist")

def seed_system(db):
    if db.system.count_documents({}) == 0:
        system = System(
            name="name",
            description="description",
        )
        db.system.insert_one(system.to_dict())
        print("\N{GRINNING FACE} System created")
    else:
        print("\N{SMILING FACE WITH OPEN MOUTH AND COLD SWEAT} System already exist")


def seed_auth(db):
    if db.auth.count_documents({}) == 0:
        auth = AuthUser(
            username="username",
            email="email",
            password="",
            confirm_password=""
        )
        db.auth.insert_one(auth.to_dict())
        print("\N{GRINNING FACE} Auth created")
    else:
        print("\N{SMILING FACE WITH OPEN MOUTH AND COLD SWEAT} Auth already exist")

def seed_telemetry_pd(db):
    if db.telemetry_per_day.count_documents({}) == 0:

        telemetry_pd = TelemetryPerDay(
            avg_temperature="avg_temperature",
            avg_humidity="avg_humidity",
            avg_co2="avg_co2",
            avg_pm25="avg_pm25",
            updated_at="updated_at",
            _id="_id"
        )
        db.telemetry_per_day.insert_one(telemetry_pd.to_dict())
        print("\N{GRINNING FACE} TelemetryPerDay created")
    else:
        print("\N{SMILING FACE WITH OPEN MOUTH AND COLD SWEAT} TelemetryPerDay already exist")

def seed_telemetry_ph(db):
    if db.telemetry_per_hour.count_documents({}) == 0:
        telemetry_ph = TelemetryPerHour(
            avg_temperature="avg_temperature",
            avg_humidity="avg_humidity",
            avg_co2="avg_co2",
            avg_pm25="avg_pm25",
            updated_at="updated_at",
            _id ="_id"
        )

        db.telemetry_per_hour.insert_one(telemetry_ph.to_dict())
        print("\N{GRINNING FACE} Telemetry_per_hour created")
    else:
        print("\N{SMILING FACE WITH OPEN MOUTH AND COLD SWEAT} Telemetry already exist")


def seed_telemetry(db):
    if db.telemetry.count_documents({}) == 0:
        telemetry = Telemetry(
            temperature="temperature",
            humidity="humidity",
            co2="co2",
            pm25="pm25",
            created_at="created_at",
            _id="_id"
        )

        db.telemetry.insert_one(telemetry.to_dict())
        print("\N{GRINNING FACE} Telemetry created")
    else:
        print("\N{SMILING FACE WITH OPEN MOUTH AND COLD SWEAT} Telemetry already exist")


def seed_all():
    with app.app_context():
        db = mongo_dev.db
        seed_users(db)
        seed_notifications(db)
        seed_system(db)
        seed_auth(db)
        seed_telemetry(db)
        seed_telemetry_pd(db)
        seed_telemetry_ph(db)
        print(" \N{SMILING FACE WITH SUNGLASSES} Seeding completed.")


if __name__ == "__main__":
    seed_all()
