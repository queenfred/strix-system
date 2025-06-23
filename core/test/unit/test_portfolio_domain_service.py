import sys
import os

# Agregar la ruta al proyecto para importar core desde security
sys.path.append("C:/Desarrollo/strix-system")

import pytest
from unittest.mock import MagicMock, patch
from core.services.portfolio_domain_service import PortfolioDomainService

@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.__enter__.return_value = uow
    uow.portfolio_domains.get_all_portfolio_domains.return_value = [{"portfolio_id": 1, "domain_id": 4873}]
    uow.portfolio_domains.get_domains_by_portfolio.return_value = [4873]
    uow.portfolio_domains.get_portfolio_domain_details.return_value = {"portfolio_name": "port", "domain_name": "dom"}
    uow.portfolio_domains.create_portfolio_domain.return_value = {"portfolio_id": 1, "domain_id": 4873}
    uow.portfolio_domains.delete_portfolio_domain.return_value = True
    uow.portfolio_domains.delete_fisico_portfolio_domain.return_value = True
    return uow

@patch("core.services.portfolio_domain_service.SQLAlchemyUnitOfWork")
def test_get_all_portfolio_domains(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = PortfolioDomainService()
    result = service.get_all_relations()
    assert isinstance(result, list)
    assert result[0]["domain_id"] == 4873

@patch("core.services.portfolio_domain_service.SQLAlchemyUnitOfWork")
def test_create_portfolio_domain(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = PortfolioDomainService()
    result = service.link_domain_to_portfolio(1, 4873, state=True, fecha_baja=None)
    assert result["portfolio_id"] == 1
    mock_uow.portfolio_domains.create_portfolio_domain.assert_called_once_with(1, 4873, state=True, fecha_baja=None)

@patch("core.services.portfolio_domain_service.SQLAlchemyUnitOfWork")
def test_delete_portfolio_domain(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = PortfolioDomainService()
    result = service.unlink_domain(1, 4873)
    assert result is True

@patch("core.services.portfolio_domain_service.SQLAlchemyUnitOfWork")
def test_delete_fisico_portfolio_domain(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = PortfolioDomainService()
    result = service.unlink_domain_fisico(1, 4873)
    assert result is True

@patch("core.services.portfolio_domain_service.SQLAlchemyUnitOfWork")
def test_get_domains_by_portfolio(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = PortfolioDomainService()
    result = service.get_domains_by_portfolio(1)
    assert 4873 in result

@patch("core.services.portfolio_domain_service.SQLAlchemyUnitOfWork")
def test_get_portfolio_domain_details(mock_uow_class, mock_uow):
    mock_uow_class.return_value = mock_uow
    service = PortfolioDomainService()
    result = service.get_relation_details(1, 4873)
    assert result["portfolio_name"] == "port"
