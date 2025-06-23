import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import pytest
from unittest.mock import MagicMock, patch
from core.services.domain_service import DomainService

@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.__enter__.return_value = uow
    uow.domains.get_all_domains.return_value = [{"id": 1, "domain": "ABC123"}]
    uow.domains.get_domain_by_id.return_value = {"id": 1, "domain": "ABC123"}
    uow.domains.get_domain_by_name.return_value = {"id": 1, "domain": "ABC123"}
    uow.domains.get_domain_by_name_and_account.return_value = {"id": 1, "domain": "ABC123", "id_account": 10}
    uow.domains.get_domains_by_names.return_value = [{"domain": "ABC123"}, {"domain": "DEF456"}]
    uow.domains.create_domain.return_value = {"id": 2, "domain": "NEW"}
    uow.domains.delete_domain.return_value = True
    uow.domains.get_existing_domains_by_name_and_account.return_value = [("ABC123", 10)]
    return uow

@patch("core.services.domain_service.SQLAlchemyUnitOfWork")
def test_get_all_domains(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    svc = DomainService()
    result = svc.get_all_domains()
    assert isinstance(result, list)

@patch("core.services.domain_service.SQLAlchemyUnitOfWork")
def test_get_domain_by_id(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    svc = DomainService()
    result = svc.get_domain_by_id(1)
    assert result["domain"] == "ABC123"

@patch("core.services.domain_service.SQLAlchemyUnitOfWork")
def test_get_domain_by_name(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    svc = DomainService()
    result = svc.get_domain_by_name("ABC123")
    assert result["domain"] == "ABC123"

@patch("core.services.domain_service.SQLAlchemyUnitOfWork")
def test_get_domain_by_name_and_account(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    svc = DomainService()
    result = svc.get_domain_by_name_and_account("ABC123", 10)
    assert result["id_account"] == 10

@patch("core.services.domain_service.SQLAlchemyUnitOfWork")
def test_get_domains_by_names(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    svc = DomainService()
    result = svc.get_domains_by_names(["ABC123", "DEF456"])
    assert len(result) == 2

@patch("core.services.domain_service.SQLAlchemyUnitOfWork")
def test_create_domain(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    svc = DomainService()
    result = svc.create_domain("NEW")
    assert result["domain"] == "NEW"

@patch("core.services.domain_service.SQLAlchemyUnitOfWork")
def test_delete_domain(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    svc = DomainService()
    result = svc.delete_domain(1)
    assert result is True

@patch("core.services.domain_service.SQLAlchemyUnitOfWork")
def test_get_existing_domains_by_name_and_account(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    svc = DomainService()
    result = svc.get_existing_domains_by_name_and_account()
    assert ("ABC123", 10) in result

@patch("core.services.domain_service.S3EventService")
def test_process_domain_id_events_success(mock_s3_service_class):
    mock_s3_service = MagicMock()
    mock_s3_service.retrieve_and_store_events.return_value = True
    mock_s3_service_class.return_value = mock_s3_service

    service = DomainService()
    result = service.process_domain_id_events(domain_id=4873, start_date="2024-01-01", end_date="2024-01-10")

    assert result["domain_id"] == 4873
    assert result["status"] is True
    mock_s3_service.retrieve_and_store_events.assert_called_once()

@patch("core.services.domain_service.S3EventService")
def test_process_domain_id_events_failure(mock_s3_service_class):
    mock_s3_service = MagicMock()
    mock_s3_service.retrieve_and_store_events.side_effect = Exception("Simulated error")
    mock_s3_service_class.return_value = mock_s3_service

    service = DomainService()
    result = service.process_domain_id_events(domain_id=4873, start_date="2024-01-01", end_date="2024-01-10")

    assert result["domain_id"] == 4873
    assert result["success"] is False
    assert "error" in result



