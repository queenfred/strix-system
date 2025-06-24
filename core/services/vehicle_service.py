
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

            new_domains.append({
                "domain": domain_name,
                "id_thing": id_thing,
                "id_account": id_account,
                "created_datetime": current_time  # 🆕 Agregar created_datetime
            })

        if new_domains:
            self.uow.domains.bulk_insert_domains(new_domains)

        return {"success": True, "created_domains": len(new_domains)}

    def create_domains_from_vehicles(self, domains=None, limit=20000):
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

            # 🆕 Crear domain con created_datetime
            new_domain = self.uow.domains.create_domain(
                domain_name, 
                id_thing, 
                id_account, 
                current_time
            )
            if new_domain:
                created_domains.append(new_domain)

        return {"success": True, "created_domains": created_domains}

    def sync_domains_with_vehicle_dates(self):
        """
        Sincroniza las fechas de creación de domains con las fechas de strix.vvehicle
        """
        with self.uow as uow:
            return uow.domains.bulk_update_created_datetime_from_vehicle()