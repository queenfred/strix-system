import sys
import os

# Agregar la ruta al proyecto para importar core desde security
sys.path.append("C:/Desarrollo/strix-system")

import pytest
from unittest.mock import patch, MagicMock
from security.services.user_service import UserService
from security.utils.password_utils import hash_password

@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.__enter__.return_value = uow
    uow.users.get_user_by_username.return_value = None
    uow.users.get_user_by_email.return_value = None
    uow.users.create_user.return_value = {"id": 1, "username": "testuser"}
    uow.users.validate_user_credentials.return_value = {
        "user": {"id": 1, "username": "testuser"},
        "roles": [{"id": 1, "name": "admin", "permissions": []}]
    }
    uow.users.get_all_users.return_value = [{"id": 1, "username": "testuser"}]
    uow.users.get_user_by_username.return_value = {"id": 1, "username": "testuser"}
    uow.users.get_user_by_email.return_value = {"id": 1, "email": "test@example.com"}
    uow.users.deactivate_user.return_value = True
    return uow


@patch("security.services.user_service.SQLAlchemyUnitOfWork")
def test_register_user(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    mock_uow.users.get_user_by_username.return_value = None  # 🛠️ aseguramos que no exista aún
    mock_uow.users.get_user_by_email.return_value = None 
    service = UserService()
    result = service.register_user("testuser", "test@example.com", "secure123", "Test User")
    assert result["username"] == "testuser"


@patch("security.services.user_service.SQLAlchemyUnitOfWork")
def test_authenticate(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = UserService()
    result = service.authenticate("testuser", "secure123")
    assert result["user"]["username"] == "testuser"

@patch("security.services.user_service.SQLAlchemyUnitOfWork")
def test_get_user(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = UserService()
    result = service.get_user("testuser")
    assert result["id"] == 1

@patch("security.services.user_service.SQLAlchemyUnitOfWork")
def test_get_user_by_email(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = UserService()
    result = service.get_user_by_email("test@example.com")
    assert result["email"] == "test@example.com"

@patch("security.services.user_service.SQLAlchemyUnitOfWork")
def test_list_users(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = UserService()
    result = service.list_users()
    assert len(result) == 1

@patch("security.services.user_service.SQLAlchemyUnitOfWork")
def test_deactivate(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = UserService()
    result = service.deactivate(1)
    assert result is True
