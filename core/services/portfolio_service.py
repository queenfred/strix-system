
from sqlalchemy.exc import SQLAlchemyError
from core.services.s3_event_service import S3EventService
from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork

class PortfolioService:
    """
    Servicio para manejar la creación y gestión de portfolios y su relación con domains.
    """

    def __init__(self):
        self.event_service = S3EventService()

    def create_portfolio_with_domains(self, portfolio_name, domains):
        """
        Crea un nuevo portfolio si no existe y asocia los dominios.
        """
        try:
            with SQLAlchemyUnitOfWork() as uow:
                # Crear o recuperar el portfolio
                portfolio = uow.portfolios.create_portfolio(portfolio_name)
                if not portfolio or not isinstance(portfolio, dict) or "id" not in portfolio:
                    print("❌ Error al crear o recuperar el portfolio.")
                    return None

                portfolio_id = portfolio["id"]

                # Asociar los dominios al portfolio
                for domain_id in domains:
                    uow.portfolio_domains.create_portfolio_domain(portfolio_id, domain_id)

                return portfolio_id
        except SQLAlchemyError as e:
            print(f"❌ Error en PortfolioService: {e}")
            return None

    def process_portfolio_events(self, portfolio_id, start_date, end_date):
        """
        Procesa eventos para todos los domain_id asociados a un portfolio sin iterar individualmente.
        """
        try:
            with SQLAlchemyUnitOfWork() as uow:
                domain_ids = uow.portfolio_domains.get_domains_by_portfolio(portfolio_id)

            if not domain_ids:
                return {"success": False, "message": "No se encontraron dominios para este portfolio."}

            results = []
            for domain_id in domain_ids:
                result = self.event_service.retrieve_and_store_events(start_date, end_date, domain_id)
                results.append({"domain_id": domain_id, "status": result})

            return {"success": True, "processed_domains": results}
        except Exception as e:
            print(f"❌ Error procesando eventos del portfolio: {e}")
            return {"success": False, "message": str(e)}

    def get_all_portfolios(self):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.portfolios.get_all_portfolios()

    def get_portfolio_by_id(self, portfolio_id):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.portfolios.get_portfolio_by_id(portfolio_id)

    def delete_portfolio(self, portfolio_id):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.portfolios.delete_portfolio(portfolio_id)        