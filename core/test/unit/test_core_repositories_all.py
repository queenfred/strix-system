import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import pytest
from unittest.mock import MagicMock
from core.data_access.domain_repository import DomainRepository
from core.data_access.vehicle_repository import VehicleRepository
from core.data_access.error_log_repository import ErrorLogRepository

@pytest.fixture
def mock_session():
    session = MagicMock()
    session.query.return_value.filter.return_value.all.return_value = []
    session.query.return_value.filter.return_value.first.return_value = MagicMock()
    session.execute.return_value.mappings.return_value.all.return_value = [{"id_thing": "THING-001", "account_id": "A1", "domain": "ABC123"}]
    return session

def test_domain_repository_get_by_id(mock_session):
    repo = DomainRepository(mock_session)
    mock_domain = MagicMock()
    mock_domain.to_dict.return_value = {"id": 4873, "domain": "ABC123"}
    mock_session.query().filter().first.return_value = mock_domain
    result = repo.get_domain_by_id(4873)
    assert result["id"] == 4873

def test_vehicle_repository_get_by_domain(mock_session):
    repo = VehicleRepository(mock_session)
    result = repo.get_vehicle_data(domains=["ABC123"], limit=1)
    assert result[0]["id_thing"] == "THING-001"

def test_error_log_repository_log_error(mock_session):
    repo = ErrorLogRepository(mock_session)
    repo.log_error("process_file", "ValueError", "archivo inválido")
    assert mock_session.add.called
    assert mock_session.commit.called
