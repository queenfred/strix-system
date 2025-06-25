import pytest
from unittest.mock import patch
from core.services.domain_service import DomainService

class TestDomainServiceSimple:
    
    @patch('core.services.domain_service.SQLAlchemyUnitOfWork')
    def test_get_all_domains_mock(self, mock_uow_class, mock_uow, sample_domain):
        # Setup mock
        mock_uow_class.return_value = mock_uow
        mock_uow.domains.get_all_domains.return_value = [sample_domain]
        
        # Test
        service = DomainService()
        result = service.get_all_domains()
        
        # Assert
        assert len(result) == 1
        assert result[0]["domain"] == "TEST123"
        mock_uow.domains.get_all_domains.assert_called_once()

    def test_domain_service_creation(self):
        """Test que solo verifica que se puede crear la instancia"""
        service = DomainService()
        assert service is not None
