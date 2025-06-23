import sys
import os

# Agregar la ruta al proyecto para importar core desde security
sys.path.append("C:/Desarrollo/strix-system")

import pytest
from unittest.mock import MagicMock, patch
from core.services.portfolio_service import PortfolioService

@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.__enter__.return_value = uow
    uow.portfolios.get_all_portfolios.return_value = [{"id": 1, "name": "default"}]
    uow.portfolios.get_portfolio_by_id.return_value = {"id": 1, "name": "default"}
    uow.portfolios.delete_portfolio.return_value = True
    return uow

@patch("core.services.portfolio_service.SQLAlchemyUnitOfWork")
def test_get_all_portfolios(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = PortfolioService()
    result = service.get_all_portfolios()
    assert isinstance(result, list)
    assert result[0]["name"] == "default"

@patch("core.services.portfolio_service.SQLAlchemyUnitOfWork")
def test_get_portfolio_by_id(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = PortfolioService()
    result = service.get_portfolio_by_id(1)
    assert isinstance(result, dict)
    assert result["id"] == 1

@patch("core.services.portfolio_service.SQLAlchemyUnitOfWork")
def test_delete_portfolio(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = PortfolioService()
    result = service.delete_portfolio(1)
    assert result is True
