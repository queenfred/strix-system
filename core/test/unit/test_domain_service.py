

# =============================================================================
# core/test/unit/test_domain_service.py
import pytest
from unittest.mock import patch
from core.services.domain_service import DomainService
from datetime import datetime

class TestDomainService:
    
    @patch('core.services.domain_service.SQLAlchemyUnitOfWork')
    def test_get_all_domains(self, mock_uow_class, mock_uow):
        mock_uow_class.return_value = mock_uow
        mock_uow.domains.get_all_domains.return_value = [
            {"id": 1, "domain": "ABC123", "id_thing": "thing1"},
            {"id": 2, "domain": "DEF456", "id_thing": "thing2"}
        ]
        
        service = DomainService()
        result = service.get_all_domains()
        
        assert len(result) == 2
        assert result[0]["domain"] == "ABC123"
        assert result[1]["domain"] == "DEF456"
        mock_uow.domains.get_all_domains.assert_called_once()

    @patch('core.services.domain_service.SQLAlchemyUnitOfWork')
    def test_create_domain(self, mock_uow_class, mock_uow):
        mock_uow_class.return_value = mock_uow
        mock_uow.domains.create_domain.return_value = {
            "id": 1, "domain": "NEW123", "id_thing": "thing1", "id_account": "account1"
        }
        
        service = DomainService()
        result = service.create_domain("NEW123", "thing1", "account1")
        
        assert result["domain"] == "NEW123"
        assert result["id_thing"] == "thing1"
        mock_uow.domains.create_domain.assert_called_once_with(
            "NEW123", "thing1", "account1", None
        )

    @patch('core.services.domain_service.SQLAlchemyUnitOfWork')
    def test_create_domain_with_datetime(self, mock_uow_class, mock_uow):
        mock_uow_class.return_value = mock_uow
        test_datetime = datetime.utcnow()
        mock_uow.domains.create_domain.return_value = {
            "id": 1, "domain": "NEW123", "created_datetime": test_datetime.isoformat()
        }
        
        service = DomainService()
        result = service.create_domain_with_current_datetime("NEW123", "thing1", "account1")
        
        assert result["domain"] == "NEW123"
        mock_uow.domains.create_domain.assert_called_once()

    @patch('core.services.domain_service.SQLAlchemyUnitOfWork')
    def test_get_domain_by_id(self, mock_uow_class, mock_uow):
        mock_uow_class.return_value = mock_uow
        mock_uow.domains.get_domain_by_id.return_value = {
            "id": 1, "domain": "TEST123", "id_thing": "thing1"
        }
        
        service = DomainService()
        result = service.get_domain_by_id(1)
        
        assert result["id"] == 1
        assert result["domain"] == "TEST123"
        mock_uow.domains.get_domain_by_id.assert_called_once_with(1)

    @patch('core.services.domain_service.SQLAlchemyUnitOfWork')
    def test_get_domain_by_name(self, mock_uow_class, mock_uow):
        mock_uow_class.return_value = mock_uow
        mock_uow.domains.get_domain_by_name.return_value = {
            "id": 1, "domain": "TEST123"
        }
        
        service = DomainService()
        result = service.get_domain_by_name("TEST123")
        
        assert result["domain"] == "TEST123"
        mock_uow.domains.get_domain_by_name.assert_called_once_with("TEST123")

    @patch('core.services.domain_service.SQLAlchemyUnitOfWork')
    def test_delete_domain(self, mock_uow_class, mock_uow):
        mock_uow_class.return_value = mock_uow
        mock_uow.domains.delete_domain.return_value = True
        
        service = DomainService()
        result = service.delete_domain(1)
        
        assert result is True
        mock_uow.domains.delete_domain.assert_called_once_with(1)

    @patch('core.services.domain_service.SQLAlchemyUnitOfWork')
    def test_bulk_update_created_datetime_from_vehicle(self, mock_uow_class, mock_uow):
        mock_uow_class.return_value = mock_uow
        mock_uow.domains.bulk_update_created_datetime_from_vehicle.return_value = 5
        
        service = DomainService()
        result = service.bulk_update_created_datetime_from_vehicle()
        
        assert result == 5
        mock_uow.domains.bulk_update_created_datetime_from_vehicle.assert_called_once()
