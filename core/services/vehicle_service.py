# core/services/vehicle_service.py
from datetime import datetime

class VehicleService:
    """
    Servicio para crear domains a partir de vehículos obtenidos de una base externa,
    utilizando UnitOfWork externo para garantizar atomicidad y reutilización.
    """

    def __init__(self, uow):
        self.uow = uow

    def create_domains_from_vehicles_bulk(self, domains=None, limit=1):
        """
        Crea domains en bulk a partir de datos de vehículos de strix.vvehicle.
        """
        with self.uow as uow:
            vehicles = uow.vehicles.get_vehicle_data(domains, limit)        

        if not vehicles:
            return {"success": False, "message": "No se encontraron vehículos en strix.vvehicle."}

        existing_domains = self.uow.domains.get_existing_domains_by_name_and_account()
        existing_keys = {(d.domain, d.id_account) for d in existing_domains}

        new_domains = []
        current_time = datetime.utcnow()  # Fecha actual para todos los nuevos domains
        
        for vehicle in vehicles:
            domain_name = vehicle["domain"]
            id_thing = vehicle["id_thing"]
            id_account = vehicle["account_id"]

            if (domain_name, id_account) in existing_keys:
                print(f"⚠️ El dominio '{domain_name}' con id_account '{id_account}' ya existe. No se creará.")
                continue

            # Crear domain con todos los campos disponibles
            new_domain = {
                "domain": domain_name,
                "id_thing": id_thing,
                "id_account": id_account,
                "created_datetime": current_time,
                "subtype": vehicle.get("subtype"),
                "color": vehicle.get("color"),
                "make": vehicle.get("make"),
                "model": vehicle.get("model"),
                "year": vehicle.get("year"),
                "gps": vehicle.get("gps")
            }
            
            new_domains.append(new_domain)

        if new_domains:
            self.uow.domains.bulk_insert_domains(new_domains)

        return {"success": True, "created_domains": len(new_domains)}

    def create_domains_from_vehicles(self, domains=None, limit=20000):
        """
        Crea domains individualmente a partir de datos de vehículos de strix.vvehicle.
        """
        with self.uow as uow:
            vehicles = uow.vehicles.get_vehicle_data(domains, limit)
        
        if not vehicles:
            return {"success": False, "message": "No se encontraron vehículos en strix.vvehicle."}

        created_domains = []
        current_time = datetime.utcnow()  # Fecha actual para nuevos domains
        
        for vehicle in vehicles:
            domain_name = vehicle["domain"]
            id_thing = vehicle["id_thing"]
            id_account = vehicle["account_id"]

            existing_domain = self.uow.domains.get_domain_by_name_and_account(domain_name, id_account)
            if existing_domain:
                print(f"⚠️ El dominio '{domain_name}' con id_account '{id_account}' ya existe. No se creará.")
                continue

            # Crear domain con todos los campos disponibles
            new_domain = self.uow.domains.create_domain(
                domain_name=domain_name, 
                id_thing=id_thing, 
                id_account=id_account, 
                created_datetime=current_time,
                subtype=vehicle.get("subtype"),
                color=vehicle.get("color"),
                make=vehicle.get("make"),
                model=vehicle.get("model"),
                year=vehicle.get("year"),
                gps=vehicle.get("gps")
            )
            if new_domain:
                created_domains.append(new_domain)

        return {"success": True, "created_domains": created_domains}

    def sync_domains_with_vehicle_data(self):
        """
        Sincroniza domains existentes con datos actualizados de strix.vvehicle
        (fechas de creación y nuevos campos de vehículo).
        """
        with self.uow as uow:
            # Primero sincronizar las fechas de creación
            updated_dates = uow.domains.bulk_update_created_datetime_from_vehicle()
            
            # Luego sincronizar los campos de vehículo
            updated_fields = uow.domains.bulk_update_vehicle_fields_from_vehicle()
            
            return {
                "success": True, 
                "updated_dates": updated_dates,
                "updated_fields": updated_fields
            }

    def sync_domains_with_vehicle_dates(self):
        """
        Sincroniza las fechas de creación de domains con las fechas de strix.vvehicle
        """
        with self.uow as uow:
            return uow.domains.bulk_update_created_datetime_from_vehicle()

    def update_domain_vehicle_info(self, domain_id, vehicle_data):
        """
        Actualiza información específica de vehículo para un domain existente.
        
        Args:
            domain_id (int): ID del domain a actualizar
            vehicle_data (dict): Datos del vehículo con campos como subtype, color, make, etc.
        """
        with self.uow as uow:
            domain = uow.domains.get_domain_by_id(domain_id)
            if not domain:
                return {"success": False, "message": f"Domain con ID {domain_id} no encontrado."}

            return uow.domains.update_domain_vehicle_fields(
                domain_id=domain_id,
                subtype=vehicle_data.get("subtype"),
                color=vehicle_data.get("color"),
                make=vehicle_data.get("make"),
                model=vehicle_data.get("model"),
                year=vehicle_data.get("year"),
                gps=vehicle_data.get("gps")
            )

    def get_domains_by_vehicle_criteria(self, make=None, model=None, year=None, color=None):
        """
        Obtiene domains filtrados por criterios de vehículo.
        
        Args:
            make (str, optional): Marca del vehículo
            model (str, optional): Modelo del vehículo
            year (int, optional): Año del vehículo
            color (str, optional): Color del vehículo
            
        Returns:
            list: Lista de domains que coinciden con los criterios
        """
        with self.uow as uow:
            return uow.domains.get_domains_by_vehicle_criteria(
                make=make, 
                model=model, 
                year=year, 
                color=color
            )