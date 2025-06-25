
# =============================================================================
# core/test/unit/test_portfolio_service.py
import pytest
from unittest.mock import patch, MagicMock
from core.services.portfolio_service import PortfolioService
from datetime import datetime

class TestPortfolioService:
    
    @patch('core.services.portfolio_service.SQLAlchemyUnitOfWork')
    @patch('core.services.portfolio_service.S3EventService')
    def test_create_portfolio_with_domains(self, mock_s3_service_class, mock_uow_class, mock_uow):
        mock_uow_class.return_value = mock_uow
        mock_uow.portfolios.create_portfolio.return_value = {"id": 1, "name": "Test Portfolio"}
        mock_uow.portfolio_domains.create_portfolio_domain.return_value = True
        
        service = PortfolioService()
        result = service.create_portfolio_with_domains("Test Portfolio", [1, 2, 3])
        
        assert result == 1
        mock_uow.portfolios.create_portfolio.assert_called_once_with("Test Portfolio")
        assert mock_uow.portfolio_domains.create_portfolio_domain.call_count == 3

    @patch('core.services.portfolio_service.SQLAlchemyUnitOfWork')
    def test_get_all_portfolios(self, mock_uow_class, mock_uow):
        mock_uow_class.return_value = mock_uow
        mock_uow.portfolios.get_all_portfolios.return_value = [
            {"id": 1, "name": "Portfolio 1"},
            {"id": 2, "name": "Portfolio 2"}
        ]
        
        service = PortfolioService()
        result = service.get_all_portfolios()
        
        assert len(result) == 2
        assert result[0]["name"] == "Portfolio 1"

    @patch('core.services.portfolio_service.SQLAlchemyUnitOfWork')
    def test_get_portfolio_by_id(self, mock_uow_class, mock_uow):
        mock_uow_class.return_value = mock_uow
        mock_uow.portfolios.get_portfolio_by_id.return_value = {"id": 1, "name": "Test Portfolio"}
        
        service = PortfolioService()
        result = service.get_portfolio_by_id(1)
        
        assert result["id"] == 1
        assert result["name"] == "Test Portfolio"

    @patch('core.services.portfolio_service.SQLAlchemyUnitOfWork')
    @patch('core.services.portfolio_service.S3EventService')
    def test_process_portfolio_events(self, mock_s3_service_class, mock_uow_class, mock_uow):
        mock_uow_class.return_value = mock_uow
        mock_uow.portfolio_domains.get_domains_by_portfolio.return_value = [1, 2]
        
        mock_s3_service = MagicMock()
        mock_s3_service_class.return_value = mock_s3_service
        mock_s3_service.retrieve_and_store_events.return_value = "SUCCESS"
        
        service = PortfolioService()
        result = service.process_portfolio_events(1, "2024-01-01", "2024-01-02")
        
        assert result["success"] is True
        assert len(result["processed_domains"]) == 2
        assert mock_s3_service.retrieve_and_store_events.call_count == 2
