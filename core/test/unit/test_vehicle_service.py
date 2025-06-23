import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import pytest
from unittest.mock import patch, MagicMock
from core.services.vehicle_service import VehicleService

@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.__enter__.return_value = uow
    uow.domains.get_existing_domains_by_name_and_account.return_value = [("ABC123", 1)]
    uow.domains.bulk_insert_domains.return_value = True
    uow.domains.get_domain_by_name_and_account.side_effect = lambda d, a: None if d == "NEW123" else {"id": 10}
    uow.domains.create_domain.return_value = {"id": 99, "domain": "NEW123"}
    uow.vehicles.get_vehicle_data.return_value = [
        {"domain": "ABC123", "id_thing": "THING001", "account_id": 1},
        {"domain": "NEW123", "id_thing": "THING002", "account_id": 2},
    ]
    return uow

@patch("core.services.vehicle_service.SQLAlchemyUnitOfWork")
def test_create_domains_from_vehicles_bulk(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = VehicleService()

    created = service.create_domains_from_vehicles_bulk(domains=None, limit=1)
    assert created == 1
    mock_uow.domains.bulk_insert_domains.assert_called_once()

@patch("core.services.vehicle_service.SQLAlchemyUnitOfWork")
def test_create_domains_from_vehicles(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = VehicleService()

    vehicles = [
        {"domain": "ABC123", "id_thing": "THING001", "account_id": 1},
        {"domain": "NEW123", "id_thing": "THING002", "account_id": 2},
    ]

    result = service.create_domains_from_vehicles(vehicles)
    assert result["success"] is True
    assert len(result["created_domains"]) == 1
    assert result["created_domains"][0]["domain"] == "NEW123"
