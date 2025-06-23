import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import pytest
from unittest.mock import MagicMock
from core.data_access.event_repository import EventRepository
from core.data_access.portfolio_domain_repository import PortfolioDomainRepository

@pytest.fixture
def mock_session():
    mock = MagicMock()
    # Mocks encadenados: .query().filter().all() y .first()
    mock_event = MagicMock()
    mock_event.to_dict.return_value = {"event_id": 284758, "domain_id": 4873}
    mock.query.return_value.filter.return_value.all.return_value = [mock_event]
    mock.query.return_value.filter.return_value.first.return_value = mock_event
    return mock

def test_event_repository_get_events_by_domain(mock_session):
    repo = EventRepository(mock_session)
    result = repo.get_events_by_domain(id_domain=4873)
    assert isinstance(result, list)
    assert result[0]["event_id"] == 284758

def test_event_repository_delete_event(mock_session):
    repo = EventRepository(mock_session)
    result = repo.delete_event(event_id=284758)
    assert result is True
    mock_session.delete.assert_called()

def test_portfolio_domain_repository_get_details(mock_session):
    repo = PortfolioDomainRepository(mock_session)
    mock_result = MagicMock()
    mock_result.portfolio_name = "PORT-102"
    mock_result.domain_name = "DOMAIN-4873"
    mock_result.id_thing = "THING-999"
    mock_result.id_account = "ACC-123"
    mock_result.state = True
    mock_result.fecha_alta = None
    mock_result.fecha_baja = None
    mock_session.query().join().join().filter().first.return_value = mock_result

    result = repo.get_portfolio_domain_details(portfolio_id=102, domain_id=4873)
    assert isinstance(result, dict)
    assert result["portfolio_name"] == "PORT-102"
    assert result["domain_name"] == "DOMAIN-4873"