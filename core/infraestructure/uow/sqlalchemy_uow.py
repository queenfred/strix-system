from core.infraestructure.db.session import SessionFactory

from core.data_access.domain_repository import DomainRepository
from core.data_access.vehicle_repository import VehicleRepository
from core.data_access.portfolio_repository import PortfolioRepository
from core.data_access.event_repository import EventRepository
from core.data_access.error_log_repository import ErrorLogRepository
from core.data_access.portfolio_domain_repository import PortfolioDomainRepository

from security.data_access.user_repository import UserRepository
from security.data_access.user_access_repository import UserAccessRepository
from security.data_access.permission_repository import PermissionRepository
from security.data_access.role_repository import RoleRepository

from reports.incident.data_access.incident_repository import IncidentRepository


from core.infraestructure.uow.abstract import IUnitOfWork

class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __enter__(self):
        SessionFactory.initialize()
        self.session = SessionFactory.get_session()

        # Repositorios core
        self.domains = DomainRepository(self.session)
        self.vehicles = VehicleRepository(self.session)
        self.portfolios = PortfolioRepository(self.session)
        self.events = EventRepository(self.session)
        self.errors = ErrorLogRepository(self.session)
        self.portfolio_domains = PortfolioDomainRepository(self.session)  # contiene get_portfolio_domain_details


        # Repositorios security
        self.users = UserRepository(self.session)
        self.permissions = PermissionRepository(self.session)
        self.roles = RoleRepository(self.session)
        self.user_access = UserAccessRepository(self.session)

        self.incidents  =IncidentRepository(self.session)

        print("🚨 ENTER: Se abrió una nueva conexión SQLAlchemy")  # Log claro

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

