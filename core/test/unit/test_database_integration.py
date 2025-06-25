
# =============================================================================
# core/test/integration/test_database_integration.py
import pytest
from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from core.services.domain_service import DomainService
from core.services.portfolio_service import PortfolioService
from core.services.event_service import EventService

@pytest.mark.integration
class TestDatabaseIntegration:
    """Tests que requieren conexión real a la base de datos"""
    
    def test_domain_crud_operations(self):
        """Test completo de operaciones CRUD en dominios"""
        service = DomainService()
        
        # Crear
        domain_data = service.create_domain("TEST_INTEGRATION", "test_thing", "test_account")
        assert domain_data is not None
        domain_id = domain_data["id"]
        
        try:
            # Leer
            retrieved = service.get_domain_by_id(domain_id)
            assert retrieved["domain"] == "TEST_INTEGRATION"
            
            # Buscar por nombre
            by_name = service.get_domain_by_name("TEST_INTEGRATION")
            assert by_name["id"] == domain_id
            
        finally:
            # Limpiar - Eliminar
            deleted = service.delete_domain(domain_id)
            assert deleted is True
            
            # Verificar eliminación
            not_found = service.get_domain_by_id(domain_id)
            assert not_found is None

    def test_portfolio_operations(self):
        """Test de operaciones de portfolio"""
        portfolio_service = PortfolioService()
        domain_service = DomainService()
        
        # Crear dominio de prueba
        domain = domain_service.create_domain("PORTFOLIO_TEST", "thing", "account")
        domain_id = domain["id"]
        
        try:
            # Crear portfolio con dominio
            portfolio_id = portfolio_service.create_portfolio_with_domains(
                "Test Portfolio Integration", [domain_id]
            )
            assert portfolio_id is not None
            
            # Verificar que se creó
            portfolio = portfolio_service.get_portfolio_by_id(portfolio_id)
            assert portfolio["name"] == "Test Portfolio Integration"
            
        finally:
            # Limpiar
            portfolio_service.delete_portfolio(portfolio_id)
            domain_service.delete_domain(domain_id)

    def test_uow_transaction_rollback(self):
        """Test que verifica el rollback de transacciones"""
        domain_id = None
        
        try:
            with SQLAlchemyUnitOfWork() as uow:
                # Crear un domain
                domain = uow.domains.create_domain("ROLLBACK_TEST", "thing", "account")
                assert domain is not None
                domain_id = domain["id"]
                
                # Forzar un error para probar rollback
                raise Exception("Forced error for testing")
                
        except Exception:
            pass
        
        # Verificar que el domain no se guardó debido al rollback
        if domain_id:
            service = DomainService()
            not_found = service.get_domain_by_id(domain_id)
            assert not_found is None

    def test_uow_transaction_commit(self):
        """Test que verifica el commit de transacciones"""
        domain_id = None
        
        try:
            with SQLAlchemyUnitOfWork() as uow:
                # Crear un domain
                domain = uow.domains.create_domain("COMMIT_TEST", "thing", "account")
                assert domain is not None
                domain_id = domain["id"]
                # No hay excepción, debería hacer commit automático
            
            # Verificar que se guardó
            service = DomainService()
            found = service.get_domain_by_id(domain_id)
            assert found is not None
            assert found["domain"] == "COMMIT_TEST"
            
        finally:
            # Limpiar
            if domain_id:
                service = DomainService()
                service.delete_domain(domain_id)
