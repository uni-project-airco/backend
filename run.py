from app import create_app
from app import scheduler
import atexit
from app.jobs import store_per_hour, store_per_day

app = create_app()

if __name__ == "__main__":
    scheduler.add_job(func=store_per_hour, trigger="interval", minutes=60)
    scheduler.add_job(func=store_per_day, trigger="interval", minutes=60)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    app.run(debug=True)
