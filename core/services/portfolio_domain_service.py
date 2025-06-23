from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork

class PortfolioDomainService:
    """
    Servicio para manejar relaciones entre Portfolio y Domain.
    """

    def get_all_relations(self):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.portfolio_domains.get_all_portfolio_domains()

    def link_domain_to_portfolio(self, portfolio_id, domain_id, state=True, fecha_baja=None):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.portfolio_domains.create_portfolio_domain(portfolio_id, domain_id, state=state, fecha_baja=fecha_baja)

    def unlink_domain(self, portfolio_id, domain_id):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.portfolio_domains.delete_portfolio_domain(portfolio_id, domain_id)

    def unlink_domain_fisico(self, portfolio_id, domain_id):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.portfolio_domains.delete_fisico_portfolio_domain(portfolio_id, domain_id)

    def get_domains_by_portfolio(self, portfolio_id):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.portfolio_domains.get_domains_by_portfolio(portfolio_id)

    def get_relation_details(self, portfolio_id, domain_id):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.portfolio_domains.get_portfolio_domain_details(portfolio_id, domain_id)