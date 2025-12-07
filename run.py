import os

from app import create_app
from app import scheduler
import atexit
from app.jobs import store_per_hour, store_per_day

app = create_app()

def hourly_job():
    with app.app_context():
        store_per_hour()

def daily_job():
    with app.app_context():
        store_per_day()

if __name__ == "__main__":
    scheduler.add_job(hourly_job, "interval", minutes=60)
    scheduler.add_job(daily_job, "interval", hours=24)

    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    app.run(debug=os.getenv("DEVELOPMENT", False))