import pytest
from unittest.mock import Mock, MagicMock

from services.user_service import UserService
from user.models import CustomUser, OneTimePassword
from user import tasks


@pytest.fixture
def user_repo():
    return Mock()


@pytest.fixture
def temp_password_repo():
    return Mock()


@pytest.fixture
def service(user_repo, temp_password_repo):
    return UserService(user_repo, temp_password_repo)


@pytest.fixture
def user():
    return MagicMock(spec=CustomUser, email="test@example.com", first_name="John", last_name="Doe", phone_number="123456789")


@pytest.fixture
def otp():
    otp_mock = MagicMock(spec=OneTimePassword)
    otp_mock.code = "temp123"
    otp_mock.is_valid.return_value = True
    return otp_mock


def test_create_temp_password_returns_non_empty_string(service):
    password = service.create_temp_password()
    assert isinstance(password, str)
    assert len(password) >= 8


def test_send_password_to_user_sends_email(service, mocker):
    mock_delay = mocker.patch.object(tasks.send_email_task, "delay")

    email = "test@example.com"
    password = "temp123"  # pragma: allowlist secret

    service.send_password_to_user(email, password)

    mock_delay.assert_called_once_with(email, password)


def test_create_user_calls_repo_with_correct_data(service, user_repo):
    data = {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "123456789",
    }

    user_mock = Mock()
    user_repo.create_user.return_value = user_mock

    result = service.create_user(data)

    user_repo.create_user.assert_called_once_with(email="test@example.com", first_name="John", last_name="Doe", phone_number="123456789")
    assert result == user_mock


def test_login_user_success(service, user_repo, temp_password_repo, user, mocker):
    user_repo.get_user.return_value = user
    mocker.patch.object(service, "create_temp_password", return_value="abc123")
    mock_send = mocker.patch.object(service, "send_password_to_user")

    result = service.login_user("test@example.com")

    temp_password_repo.create_temporary_password.assert_called_once_with(user, "abc123")
    mock_send.assert_called_once_with("test@example.com", "abc123")
    assert result == user


def test_login_user_user_not_found(service, user_repo):
    user_repo.get_user.return_value = None

    result = service.login_user("notfound@example.com")

    assert result is None


def test_get_or_create_user_existing_user(service, user_repo, user):
    user_repo.get_user.return_value = user

    data = {"email": "test@example.com"}
    result = service.get_or_create_user(data)

    user_repo.get_user.assert_called_once_with("test@example.com")
    assert result == user


def test_get_or_create_user_creates_if_not_exists(service, user_repo, user):
    user_repo.get_user.return_value = None
    user_repo.create_user.return_value = user

    data = {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "123456789",
    }

    result = service.get_or_create_user(data)

    user_repo.create_user.assert_called_once()
    assert result == user


def test_check_user_data_updates_if_differs(service, user_repo, user):
    user.first_name = "Old"
    data = {"first_name": "New", "last_name": "Doe", "phone_number": "123456789"}

    service.check_user_data(user, data)

    user_repo.update_user.assert_called_once_with(user, data)


def test_check_user_data_no_update_if_same(service, user_repo, user):
    data = {"first_name": user.first_name, "last_name": user.last_name, "phone_number": user.phone_number}

    service.check_user_data(user, data)

    user_repo.update_user.assert_not_called()


def test_authenticate_user_success(service, user_repo, temp_password_repo, user, otp):
    user_repo.get_user.return_value = user
    temp_password_repo.get_valid_temporary_password.return_value = otp

    result = service.authenticate_user("test@example.com", "temp123")

    assert result == user


def test_authenticate_user_wrong_password(service, user_repo, temp_password_repo, user, otp):
    user_repo.get_user.return_value = user
    otp.code = "something_else"
    temp_password_repo.get_valid_temporary_password.return_value = otp

    result = service.authenticate_user("test@example.com", "wrong")

    assert result is None


def test_authenticate_user_no_user(service, user_repo):
    user_repo.get_user.return_value = None

    result = service.authenticate_user("notfound@example.com", "temp123")

    assert result is None


def test_authenticate_user_no_otp(service, user_repo, temp_password_repo, user):
    user_repo.get_user.return_value = user
    temp_password_repo.get_valid_temporary_password.return_value = None

    result = service.authenticate_user("test@example.com", "temp123")

    assert result is None


def test_is_email_free_returns_value_from_repo(service, user_repo):
    user_repo.is_email_free.return_value = True
    assert service.is_email_free("some@email.com") is True


def test_is_phone_free_returns_value_from_repo(service, user_repo):
    user_repo.is_phone_free.return_value = False
    assert service.is_phone_free("123456789") is False
