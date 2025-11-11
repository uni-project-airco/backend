import pytest
from unittest.mock import patch, MagicMock
from werkzeug.security import generate_password_hash

from app.auth.views import loginUser, registerUser, refreshToken

@pytest.fixture
def mock_request():
    """Helper to simulate Flask request with JSON data."""
    class MockRequest:
        def __init__(self, json_data):
            self._json = json_data

        def get_json(self):
            return self._json
    return MockRequest

# Test registerUser
@patch("app.auth.views.mongoDB")
@patch("app.auth.views.User")
@patch("app.auth.views.create_access_token", return_value="fake_access")
@patch("app.auth.views.create_refresh_token", return_value="fake_refresh")
def test_register_user_success(mock_refresh, mock_access, mock_user, mock_db, mock_request):
    request = mock_request({"username": "testuser", "password": "pass123"})

    user_instance = MagicMock()
    user_instance.username = "testuser"
    user_instance.id = "1"
    mock_user.from_mongo.return_value = user_instance

    mock_db.db = MagicMock()
    mock_db.db.users = MagicMock()
    mock_db.db.users.find_one.return_value = None 

    result, status = registerUser(request)

    assert status == 200
    assert result["msg"] == "User successfully registered and logged in"
    assert result["access_token"] == "fake_access"
    assert result["refresh_token"] == "fake_refresh"

@patch("app.auth.views.mongoDB")
@patch("app.auth.views.User")
def test_register_user_alreay_exist(mock_user, mock_db, mock_request):
    request = mock_request({"username": "existing", "password": "pass123"})

    user_instance = MagicMock()
    user_instance.username = "existing"
    mock_user.from_mongo.return_value = user_instance

    mock_db.db.users.find_one.return_value = user_instance

    result = registerUser(request)

    assert result == {"msg": "You already have an account. Try Login"}

# Test loginUser
@patch("app.auth.views.mongoDB")
@patch("app.auth.views.create_access_token", return_value="fake_access")
@patch("app.auth.views.create_refresh_token", return_value="fake_refresh")
def test_login_user_success(mock_refresh, mock_access, mock_db, mock_request):
    password = "pass123"
    hashed = generate_password_hash(password)

    request = mock_request({"username": "testuser", "password": password})
    mock_db.db.users.find_one.return_value = {"_id": "123", "username": "testuser", "password": hashed}

    result, status = loginUser(request)
    assert status == 200
    assert result["access_token"] == "fake_access"
    assert result["refresh_token"] == "fake_refresh"


@patch("app.auth.views.mongoDB")
def test_login_user_bad_credentials(mock_db, mock_request):
    request = mock_request({"username": "wrong", "password": "bad"})
    mock_db.db.users.find_one.return_value = None

    result, status = loginUser(request)
    assert status == 403
    assert result["msg"] == "Bad credentials"

# Test refreshToken
@patch("app.auth.views.create_access_token", return_value="new_token")
@patch("app.auth.views.get_jwt_identity", return_value="1")
def test_refresh_token(mock_identity, mock_access):
    result, status = refreshToken()
    assert status == 200
    assert result["access_token"] == "new_token"
