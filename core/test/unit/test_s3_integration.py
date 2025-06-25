
# =============================================================================
# core/test/integration/test_s3_integration.py
import pytest
from unittest.mock import patch
from core.infraestructure.aws.s3 import S3Client
from core.services.s3_event_service import S3EventService

@pytest.mark.integration
class TestS3Integration:
    """Tests de integración con S3 (requieren configuración real)"""
    
    @pytest.mark.skip(reason="Requiere configuración real de S3")
    def test_s3_connection(self):
        """Test de conexión real a S3"""
        s3_client = S3Client()
        client = s3_client.conn_s3()
        
        assert client is not None
        
        # Test listar buckets (si tienes permisos)
        buckets = s3_client.list_buckets()
        assert buckets is not None

    def test_s3_client_mock_integration(self):
        """Test de integración con S3 usando mocks"""
        with patch('core.infraestructure.aws.s3.boto3.client') as mock_boto3:
            mock_client = mock_boto3.return_value
            mock_client.list_buckets.return_value = {
                'Buckets': [{'Name': 'test-bucket'}]
            }
            
            s3_client = S3Client()
            client = s3_client.conn_s3()
            buckets = s3_client.list_buckets()
            
            assert client is not None
            assert 'test-bucket' in buckets
