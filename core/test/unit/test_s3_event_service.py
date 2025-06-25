
# =============================================================================
# core/test/unit/test_s3_event_service.py
import pytest
from unittest.mock import patch, MagicMock
from core.services.s3_event_service import S3EventService
import io

class TestS3EventService:
    
    @patch('core.services.s3_event_service.S3Client')
    @patch('core.services.s3_event_service.SQLAlchemyUnitOfWork')
    def test_retrieve_and_store_events_success(self, mock_uow_class, mock_s3_class, mock_uow):
        # Setup mocks
        mock_uow_class.return_value = mock_uow
        mock_s3_instance = MagicMock()
        mock_s3_class.return_value.conn_s3.return_value = mock_s3_instance
        mock_s3_instance.config = {'bucket_name': 'test', 'file_suffix': '.avro'}
        
        # Mock domain data
        mock_uow.portfolio_domains.get_portfolio_domain_info.return_value = {
            'account_id': 'test_account', 'id_thing': 'test_thing'
        }
        
        # Mock S3 response with avro data
        mock_response = MagicMock()
        mock_response['Body'].read.return_value = b'avro_data'
        mock_s3_instance.s3_client.get_object.return_value = mock_response
        
        service = S3EventService()
        
        with patch('core.services.s3_event_service.fastavro.reader') as mock_reader:
            mock_reader.return_value = [
                {"details": {"event": "test", "latitude": -34.6, "longitude": -58.4, 
                           "timestamp": 1234567890, "odometer": 100, "speed": 50, "heading": 90}}
            ]
            
            result = service.retrieve_and_store_events("2024-01-01", "2024-01-02", 1)
        
        assert result == "SUCCESS"
        mock_uow.events.store_events.assert_called_once()

    @patch('core.services.s3_event_service.S3Client')
    def test_retrieve_and_store_events_no_connection(self, mock_s3_class):
        mock_s3_class.return_value.conn_s3.return_value = None
        
        service = S3EventService()
        result = service.retrieve_and_store_events("2024-01-01", "2024-01-02", 1)
        
        assert result == "ERROR_S3_CONNECTION"

    @patch('core.services.s3_event_service.S3Client')
    @patch('core.services.s3_event_service.SQLAlchemyUnitOfWork')
    def test_retrieve_and_store_events_invalid_domain(self, mock_uow_class, mock_s3_class, mock_uow):
        mock_uow_class.return_value = mock_uow
        mock_s3_instance = MagicMock()
        mock_s3_class.return_value.conn_s3.return_value = mock_s3_instance
        
        # Mock invalid domain
        mock_uow.portfolio_domains.get_portfolio_domain_info.return_value = None
        
        service = S3EventService()
        result = service.retrieve_and_store_events("2024-01-01", "2024-01-02", 999)
        
        assert result == "INVALID_DOMAIN"
