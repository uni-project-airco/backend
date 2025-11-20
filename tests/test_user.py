import pytest
from unittest.mock import patch, MagicMock

from app.users.views import changeUsername, changeEmail, changePassword

@pytest.fixture
def mock_request():
    """Helper to simulate Flask request with JSON data."""
    class MockRequest:
        def __init__(self, json_data):
            self.json = json_data
    return MockRequest

#Test changeUsername
@patch("app.users.views.mongoDB")
@patch("app.users.views.User")
@patch("app.users.views.get_jwt_identity", return_value="1")
def test_change_username_success(mock_identity, mock_user, mock_db, mock_request):
    request = mock_request({"username" : "newUsername"})

    user_instance = MagicMock()
    user_instance.username = "oldUsername"
    mock_user.get_by_id.return_value = user_instance

    mock_db.db = MagicMock()
    mock_db.db.users = MagicMock()

    result, status = changeUsername(request)

    assert status == 200
    assert result["msg"] == "username is successfully changed"
    mock_db.db.users.update_one.assert_called_once_with(
        {"username": "oldUsername"}, {"$set": {"username": "newUsername"}}
    )

def test_change_username_missing_username(mock_request):
    request = mock_request({})
    with patch("app.users.views.get_jwt_identity", return_value="123"), \
         patch("app.users.views.User.get_by_id", return_value=MagicMock(username="olduser")):
        result, status = changeUsername(request)
        assert status == 400
        assert result["msg"] == "username missing"


def test_change_username_missing_userid(mock_request):
    request = mock_request({"username": "newuser"})
    with patch("app.users.views.get_jwt_identity", return_value=None):
        result, status = changeUsername(request)
        assert status == 400
        assert result["msg"] == "user_id is missing"


#Test changeEmail
@patch("app.users.views.mongoDB")
@patch("app.users.views.User")
@patch("app.users.views.get_jwt_identity", return_value="1")
def test_change_email_success(mock_identity, mock_user, mock_db, mock_request):
    request = mock_request({"email": "new@email.com"})

    user_instance = MagicMock()
    user_instance.email = "old@email.com"
    mock_user.get_by_id.return_value = user_instance

    mock_db.db = MagicMock()
    mock_db.db.users = MagicMock()

    result, status = changeEmail(request)
    assert status == 200
    assert result["msg"] == "email is successfully changed"
    mock_db.db.users.update_one.assert_called_once_with(
        {"email": "old@email.com"}, {"$set": {"email": "new@email.com"}}
    )

def test_change_email_missing_email(mock_request):
    request = mock_request({})
    with patch("app.users.views.get_jwt_identity", return_value="123"), \
         patch("app.users.views.User.get_by_id", return_value=MagicMock(email="old@email.com")):
        result, status = changeEmail(request)
        assert status == 400
        assert result["msg"] == "email missing"


def test_change_email_missing_userid(mock_request):
    request = mock_request({"email": "newEmail"})
    with patch("app.users.views.get_jwt_identity", return_value=None):
        result, status = changeUsername(request)
        assert status == 400
        assert result["msg"] == "user_id is missing"

#Test changePassword
@patch("app.users.views.mongoDB")
@patch("app.users.views.User")
@patch("app.users.views.get_jwt_identity", return_value="123")
def test_change_password_success(mock_identity, mock_user, mock_db, mock_request):
    request = mock_request({"oldPassword": "oldpass", "newPassword": "newpass"})

    user_instance = MagicMock()
    user_instance.password = "hashed_old"
    user_instance.verify_password.return_value = True
    user_instance.hash_password.return_value = "hashed_new"

    mock_user.get_by_id.return_value = user_instance
    mock_db.db = MagicMock()
    mock_db.db.users = MagicMock()

    result, status = changePassword(request)
    assert status == 200
    assert result["msg"] == "password is successfully changed"
    mock_db.db.users.update_one.assert_called_once_with(
        {"password": "hashed_old"}, {"$set": {"password": "hashed_new"}}
    )


def test_change_password_missing_fields(mock_request):
    request = mock_request({"oldPassword": "oldpass"})
    with patch("app.users.views.get_jwt_identity", return_value="123"), \
         patch("app.users.views.User.get_by_id", return_value=MagicMock()):
        result, status = changePassword(request)
        assert status == 400
        assert result["msg"] == "old password or new password missing"


def test_change_password_wrong_old_password(mock_request):
    request = mock_request({"oldPassword": "wrong", "newPassword": "newpass"})
    user_instance = MagicMock()
    user_instance.verify_password.return_value = False

    with patch("app.users.views.get_jwt_identity", return_value="123"), \
         patch("app.users.views.User.get_by_id", return_value=user_instance):
        result, status = changePassword(request)
        assert status == 403
        assert result["msg"] == "wrong password"