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

    def create_domain(self, domain_name, id_thing=None, id_account=None, created_datetime=None,
                     subtype=None, color=None, make=None, model=None, year=None, gps=None):
        """
        Crea un nuevo dominio con todos los campos disponibles
        """
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.create_domain(
                domain_name=domain_name, 
                id_thing=id_thing, 
                id_account=id_account, 
                created_datetime=created_datetime,
                subtype=subtype,
                color=color,
                make=make,
                model=model,
                year=year,
                gps=gps
            )

    def create_domain_with_current_datetime(self, domain_name, id_thing=None, id_account=None,
                                          subtype=None, color=None, make=None, model=None, 
                                          year=None, gps=None):
        """
        Crea un nuevo dominio con la fecha/hora actual
        """
        return self.create_domain(
            domain_name=domain_name, 
            id_thing=id_thing, 
            id_account=id_account, 
            created_datetime=datetime.utcnow(),
            subtype=subtype,
            color=color,
            make=make,
            model=model,
            year=year,
            gps=gps
        )

    def update_domain_created_datetime(self, domain_id, created_datetime):
        """
        Actualiza la fecha de creación de un dominio específico
        """
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.update_domain_created_datetime(domain_id, created_datetime)

    def update_domain_vehicle_info(self, domain_id, subtype=None, color=None, make=None, 
                                 model=None, year=None, gps=None):
        """
        Actualiza información del vehículo de un dominio específico
        """
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.update_domain_vehicle_fields(
                domain_id=domain_id,
                subtype=subtype,
                color=color,
                make=make,
                model=model,
                year=year,
                gps=gps
            )

    def bulk_update_created_datetime_from_vehicle(self):
        """
        Actualiza created_datetime de todos los domains usando datos de strix.vvehicle
        """
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.bulk_update_created_datetime_from_vehicle()

    def bulk_update_vehicle_fields_from_vehicle(self):
        """
        Actualiza campos de vehículo de todos los domains usando datos de strix.vvehicle
        """
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.bulk_update_vehicle_fields_from_vehicle()

    def sync_all_domain_data_from_vehicle(self):
        """
        Sincroniza tanto fechas como campos de vehículo desde strix.vvehicle
        """
        with SQLAlchemyUnitOfWork() as uow:
            updated_dates = uow.domains.bulk_update_created_datetime_from_vehicle()
            updated_fields = uow.domains.bulk_update_vehicle_fields_from_vehicle()
            
            return {
                "success": True,
                "updated_dates": updated_dates,
                "updated_fields": updated_fields,
                "total_updated": updated_dates + updated_fields
            }

    def get_domains_by_vehicle_criteria(self, make=None, model=None, year=None, color=None):
        """
        Obtiene dominios filtrados por criterios de vehículo
        """
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.get_domains_by_vehicle_criteria(
                make=make, 
                model=model, 
                year=year, 
                color=color
            )

    def get_domains_with_null_created_datetime(self):
        """
        Obtiene dominios que no tienen fecha de creación
        """
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.get_domains_with_null_created_datetime()

    def get_domain_statistics(self):
        """
        Obtiene estadísticas de los dominios por características del vehículo
        """
        with SQLAlchemyUnitOfWork() as uow:
            all_domains = uow.domains.get_all_domains()
            
            stats = {
                "total_domains": len(all_domains),
                "with_vehicle_info": len([d for d in all_domains if d.get("make")]),
                "unique_makes": len(set(d.get("make") for d in all_domains if d.get("make"))),
                "unique_models": len(set(d.get("model") for d in all_domains if d.get("model"))),
                "unique_colors": len(set(d.get("color") for d in all_domains if d.get("color"))),
                "with_created_datetime": len([d for d in all_domains if d.get("created_datetime")]),
                "without_created_datetime": len([d for d in all_domains if not d.get("created_datetime")])
            }
            
            return stats

    def delete_domain(self, domain_id):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.delete_domain(domain_id)

    def get_existing_domains_by_name_and_account(self):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.get_existing_domains_by_name_and_account()

    def get_existing_domains_by_names(self, domain_names):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.domains.get_existing_domains_by_names(domain_names)