from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from core.services.s3_event_service import S3EventService

class DomainService:
    """
    Servicio para manejar operaciones de dominio a través del repositorio y orquestar lógica de negocio.
    """

    def __init__(self):
        self.event_service = S3EventService()

    def process_domain_id_events(self, domain_id, start_date, end_date):
        try:
            result = self.event_service.retrieve_and_store_events(start_date, end_date, domain_id)
            return {"domain_id": domain_id, "status": result}
        except Exception as e:
            return {"domain_id": domain_id, "success": False, "error": str(e)}

    def get_all_domains(self):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.get_all_domains()

    def get_domain_by_id(self, domain_id):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.get_domain_by_id(domain_id)

    def get_domain_by_name(self, domain_name):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.get_domain_by_name(domain_name)

    def get_domain_by_name_and_account(self, domain_name, id_account):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.get_domain_by_name_and_account(domain_name, id_account)

    def get_domains_by_names(self, domain_names):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.get_domains_by_names(domain_names)

    def create_domain(self, domain_name, id_thing=None, id_account=None):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.create_domain(domain_name, id_thing, id_account)

    def delete_domain(self, domain_id):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.delete_domain(domain_id)

    def get_existing_domains_by_name_and_account(self):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.get_existing_domains_by_name_and_account()

    def get_existing_domains_by_names(self, domain_names):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.get_existing_domains_by_names(domain_names)        
