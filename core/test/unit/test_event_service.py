
# =============================================================================
# core/test/unit/test_event_service.py
import pytest
from unittest.mock import patch, MagicMock
from core.services.event_service import EventService
from datetime import datetime, timedelta

class TestEventService:
    
    def test_get_events_by_domain(self, mock_uow):
        mock_uow.events.get_events_by_domain.return_value = [
            {"id": 1, "id_domain": 1, "latitude": -34.6118, "longitude": -58.3960},
            {"id": 2, "id_domain": 1, "latitude": -34.6200, "longitude": -58.4000}
        ]
        
        service = EventService(mock_uow)
        
        with patch('core.services.event_service.SQLAlchemyUnitOfWork') as mock_uow_class:
            mock_uow_class.return_value.__enter__.return_value = mock_uow
            result = service.get_events_by_domain(1)
        
        assert len(result) == 2
        assert result[0]["id_domain"] == 1
        assert result[1]["id_domain"] == 1

    def test_get_events_by_domain_and_date(self, mock_uow):
        start_date = datetime.now()
        end_date = start_date + timedelta(days=1)
        
        mock_uow.events.get_events_by_domain_and_date.return_value = [
            {"id": 1, "id_domain": 1, "timestamp": 1704196800000}
        ]
        
        service = EventService(mock_uow)
        
        with patch('core.services.event_service.SQLAlchemyUnitOfWork') as mock_uow_class:
            mock_uow_class.return_value.__enter__.return_value = mock_uow
            result = service.get_events_by_domain_and_date(1, start_date, end_date)
        
        assert len(result) == 1
        assert result[0]["id_domain"] == 1
        mock_uow.events.get_events_by_domain_and_date.assert_called_once_with(1, start_date, end_date)

    def test_create_event(self, mock_uow):
        mock_uow.events.create_event.return_value = {
            "id": 1, "id_domain": 1, "latitude": -34.6118, "longitude": -58.3960,
            "speed": 50, "event": "position", "timestamp": 1704196800000, 
            "odometer": 100, "heading": 90
        }
        
        service = EventService(mock_uow)
        
        with patch('core.services.event_service.SQLAlchemyUnitOfWork') as mock_uow_class:
            mock_uow_class.return_value.__enter__.return_value = mock_uow
            result = service.create_event(1, -34.6118, -58.3960, 50, "position", 1704196800000, 100, 90)
        
        assert result["id"] == 1
        assert result["latitude"] == -34.6118
        assert result["event"] == "position"

    def test_store_events(self, mock_uow):
        events_data = [
            {"id_domain": 1, "latitude": -34.6118, "longitude": -58.3960, "speed": 50, 
             "event": "position", "timestamp": 1704196800000, "odometer": 100, "heading": 90},
            {"id_domain": 1, "latitude": -34.6200, "longitude": -58.4000, "speed": 40, 
             "event": "position", "timestamp": 1704196860000, "odometer": 101, "heading": 85}
        ]
        
        service = EventService(mock_uow)
        
        with patch('core.services.event_service.SQLAlchemyUnitOfWork') as mock_uow_class:
            mock_uow_class.return_value.__enter__.return_value = mock_uow
            service.store_events(events_data)
        
        mock_uow.events.store_events.assert_called_once_with(events_data)
