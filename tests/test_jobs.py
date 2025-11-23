import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from app.jobs import store_per_hour, store_per_day

# test store_per_hour
@patch("app.jobs.mongoDB")
def test_store_per_hour_success(mock_db):
    mock_db.db.telemetry = MagicMock()
    mock_db.db.telemetry_per_hour = MagicMock()

    now = datetime.now()

    # Create 6 fake telemetry documents
    fake_docs = [{
        "created_at": now - timedelta(minutes=i),
        "temperature": 20 + i,
        "humidity": 30 + i,
        "co2": 400 + i,
        "pm25": 5 + i
    } for i in range(6)]

    mock_db.db.telemetry.find.return_value.sort.return_value.limit.return_value = fake_docs

    store_per_hour()

    insert_args = mock_db.db.telemetry_per_hour.insert_one.call_args[0][0]

    assert insert_args["avg_temperature"] == pytest.approx(sum(20+i for i in range(6)) / 6)
    assert insert_args["avg_humidity"] == pytest.approx(sum(30+i for i in range(6)) / 6)
    assert insert_args["avg_co2"] == pytest.approx(sum(400+i for i in range(6)) / 6)
    assert insert_args["avg_pm25"] == pytest.approx(sum(5+i for i in range(6)) / 6)
    assert "updated_at" in insert_args


# test store_per_day
@patch("app.jobs.mongoDB")
def test_store_per_day_success(mock_db):
    mock_db.db.telemetry_per_hour = MagicMock()
    mock_db.db.telemetry_per_day = MagicMock()

    now = datetime.now()

    fake_docs = [{
        "created_at": now - timedelta(hours=i),
        "avg_temperature": 20 + i,
        "avg_humidity": 40 + i,
        "avg_co2": 500 + i,
        "avg_pm25": 10 + i
    } for i in range(24)]

    mock_db.db.telemetry_per_hour.find.return_value.sort.return_value.limit.return_value = fake_docs

    store_per_day()

    insert_args = mock_db.db.telemetry_per_day.insert_one.call_args[0][0]

    assert insert_args["avg_temperature"] == pytest.approx(sum(20+i for i in range(24)) / 24)
    assert insert_args["avg_humidity"] == pytest.approx(sum(40+i for i in range(24)) / 24)
    assert insert_args["avg_co2"] == pytest.approx(sum(500+i for i in range(24)) / 24)
    assert insert_args["avg_pm25"] == pytest.approx(sum(10+i for i in range(24)) / 24)
    assert "updated_at" in insert_args
