# core/services/domain_service.py
from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from core.services.s3_event_service import S3EventService
from datetime import datetime

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

    def create_domain(self, domain_name, id_thing=None, id_account=None, created_datetime=None):
        """
        Crea un nuevo dominio con fecha de creación opcional
        """
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.create_domain(domain_name, id_thing, id_account, created_datetime)

    def create_domain_with_current_datetime(self, domain_name, id_thing=None, id_account=None):
        """
        Crea un nuevo dominio con la fecha/hora actual
        """
        return self.create_domain(domain_name, id_thing, id_account, datetime.utcnow())

    def update_domain_created_datetime(self, domain_id, created_datetime):
        """
        Actualiza la fecha de creación de un dominio específico
        """
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.update_domain_created_datetime(domain_id, created_datetime)

    def bulk_update_created_datetime_from_vehicle(self):
        """
        Actualiza created_datetime de todos los domains usando datos de strix.vvehicle
        """
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.bulk_update_created_datetime_from_vehicle()

    def get_domains_with_null_created_datetime(self):
        """
        Obtiene dominios que no tienen fecha de creación
        """
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.get_domains_with_null_created_datetime()

    def delete_domain(self, domain_id):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.delete_domain(domain_id)

    def get_existing_domains_by_name_and_account(self):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.get_existing_domains_by_name_and_account()

    def get_existing_domains_by_names(self, domain_names):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.get_existing_domains_by_names(domain_names)