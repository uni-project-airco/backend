import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from app.telemetry.routes import (
    getTelemetryPerDay,
    getTelemetryPerWeek,
    getHistoricalData,
)


# ---------- Test getTelemetryPerDay ----------
@patch("app.telemetry.views.mongoDB")
def test_get_telemetry_per_day(mock_db):
    now = datetime.now()

    docs = [
        {"created_at": now - timedelta(hours=i), "value": i} 
        for i in range(24)
    ]

    # Mock: find → sort → limit returns our docs
    mock_db.db.telemetry_per_hour.find.return_value.sort.return_value.limit.return_value = docs

    result = getTelemetryPerDay()

    # Reversed list: last element should be with i=0
    assert result[0]["value"] == 23
    assert result[-1]["value"] == 0
    assert len(result) == 24


# ---------- Test getTelemetryPerWeek ----------
@patch("app.telemetry.views.mongoDB")
def test_get_telemetry_per_week(mock_db):
    now = datetime.now()

    docs = [
        {"created_at": now - timedelta(days=i), "avg": i} 
        for i in range(7)
    ]

    mock_db.db.telemetry_per_day.find.return_value.sort.return_value.limit.return_value = docs

    result = getTelemetryPerWeek()

    assert result[0]["avg"] == 6
    assert result[-1]["avg"] == 0
    assert len(result) == 7


# ---------- Test getHistoricalData (success) ----------
@patch("app.telemetry.views.mongoDB")
def test_get_historical_success(mock_db):
    now = datetime.now()

    day_docs = [{"created_at": now, "temperature": i} for i in range(24)]
    week_docs = [{"created_at": now, "avg_temp": i} for i in range(7)]

    # Patch both day + week calls
    mock_db.db.telemetry_per_hour.find.return_value.sort.return_value.limit.return_value = day_docs
    mock_db.db.telemetry_per_day.find.return_value.sort.return_value.limit.return_value = week_docs

    response, status = getHistoricalData()

    assert status == 200
    assert "day" in response
    assert "week" in response
    assert len(response["day"]) == 24
    assert len(response["week"]) == 7


# ---------- Test getHistoricalData (failure) ----------
@patch("app.telemetry.views.mongoDB")
def test_get_historical_failure(mock_db):
    # Simulate returning empty lists for both queries
    mock_db.db.telemetry_per_hour.find.return_value.sort.return_value.limit.return_value = []
    mock_db.db.telemetry_per_day.find.return_value.sort.return_value.limit.return_value = []

    response, status = getHistoricalData()

    assert status == 400
    assert response["msg"] == "Unable to find historical data"
