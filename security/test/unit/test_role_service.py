import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import pytest
from unittest.mock import patch, MagicMock
from security.services.role_service import RoleService

@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.__enter__.return_value = uow
    uow.roles.create_role.return_value = {"id": 1, "name": "admin"}
    uow.roles.get_role_by_name.return_value = {"id": 1, "name": "admin"}
    uow.roles.get_role_by_id.return_value = {"id": 1, "name": "admin"}
    uow.roles.get_all_roles.return_value = [{"id": 1, "name": "admin"}, {"id": 2, "name": "user"}]
    uow.roles.update_role.return_value = {"id": 1, "name": "superadmin"}
    uow.roles.delete_role.return_value = True
    return uow

@patch("security.services.role_service.SQLAlchemyUnitOfWork")
def test_create_role(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = RoleService()
    result = service.create_role("admin", "Administrator role")
    assert result["name"] == "admin"

@patch("security.services.role_service.SQLAlchemyUnitOfWork")
def test_get_role_by_name(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = RoleService()
    result = service.get_role_by_name("admin")
    assert result["id"] == 1

@patch("security.services.role_service.SQLAlchemyUnitOfWork")
def test_get_role_by_id(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = RoleService()
    result = service.get_role_by_id(1)
    assert result["name"] == "admin"

@patch("security.services.role_service.SQLAlchemyUnitOfWork")
def test_get_all_roles(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = RoleService()
    result = service.get_all_roles()
    assert len(result) == 2

@patch("security.services.role_service.SQLAlchemyUnitOfWork")
def test_update_role(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = RoleService()
    result = service.update_role(1, name="superadmin")
    assert result["name"] == "superadmin"

@patch("security.services.role_service.SQLAlchemyUnitOfWork")
def test_delete_role(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = RoleService()
    result = service.delete_role(1)
    assert result is True
