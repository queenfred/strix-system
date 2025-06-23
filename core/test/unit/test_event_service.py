import sys
import os
import pytest
from unittest.mock import MagicMock
from core.services.event_service import EventService

# ✅ Setup del path al root del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.events.get_event_by_id.return_value = {"id": 1, "event": "start"}
    uow.events.get_events_by_domain.return_value = [{"id": 1}, {"id": 2}]
    uow.events.get_events_by_domain_and_date.return_value = [{"id": 1}]
    uow.events.create_event.return_value = {"id": 3}
    uow.events.delete_event.return_value = True
    uow.events.store_events.return_value = {"success": True}
    return uow

def test_get_event_by_id(mock_uow):
    svc = EventService(mock_uow)
    result = svc.get_event_by_id(1)
    assert result["id"] == 1

def test_get_events_by_domain(mock_uow):
    svc = EventService(mock_uow)
    result = svc.get_events_by_domain(4873)
    assert isinstance(result, list)

def test_get_events_by_domain_and_date(mock_uow):
    svc = EventService(mock_uow)
    result = svc.get_events_by_domain_and_date(4873, "2023-01-01", "2023-01-10")
    assert isinstance(result, list)

def test_create_event(mock_uow):
    svc = EventService(mock_uow)
    result = svc.create_event(4873, -34.6, -58.4, 0, "main_power_on", 1234567890, 0.0, 340)
    assert result["id"] == 3

def test_delete_event(mock_uow):
    svc = EventService(mock_uow)
    result = svc.delete_event(1)
    assert result is True

def test_store_events(mock_uow):
    svc = EventService(mock_uow)
    dummy_events = [
        {"id_domain": 4873, "latitude": 0, "longitude": 0, "speed": 0, "event": "start", "timestamp": 1234567890, "odometer": 0, "heading": 0}
    ]
    result = svc.store_events(dummy_events)
    assert result["success"] is True
