from datetime import datetime, timezone
from app import create_app, mongo_dev
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
        print("✅ Users created")
    else:
        print("ℹ️ Users already exist")


def seed_notifications(db):
    if db.notifications.count_documents({}) == 0:
        notification = Notification(
            metric="metric",
            threshold=20.0,
            is_enabled=True
        )
        db.notifications.insert_one(notification.to_dict())
        print("✅ Notification created")
    else:
        print("ℹ️ Notification already exist")


def seed_all():
    with app.app_context():
        db = mongo_dev.db
        seed_users(db)
        seed_notifications(db)
        print("🎉 Seeding completed.")


if __name__ == "__main__":
    seed_all()
