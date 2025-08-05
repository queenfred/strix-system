# core/data_access/domain_repository.py
from core.models.domain import Domain
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class DomainRepository:
    def __init__(self, session):
        self.session = session

    def get_all_domains(self):
        try:
            domains = self.session.query(Domain).all()
            return [domain.to_dict() for domain in domains]
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener domains: {e}")
            return []

    def get_domain_by_id(self, domain_id):
        try:
            domain = self.session.query(Domain).filter(Domain.id == domain_id).first()
            return domain.to_dict() if domain else None
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener el domain con ID {domain_id}: {e}")
            return None

    def get_domain_by_name(self, domain_name):
        try:
            return self.session.query(Domain).filter_by(domain=domain_name).first()
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener el dominio por nombre: {e}")
            return None

    def get_domain_by_name_and_account(self, domain_name, id_account):
        try:
            return self.session.query(Domain).filter_by(domain=domain_name, id_account=id_account).first()
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener el dominio por nombre y cuenta: {e}")
            return None

    def get_domains_by_names(self, domain_names: list):
        try:
            return self.session.query(Domain).filter(Domain.domain.in_(domain_names)).all()
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener dominios por nombre: {e}")
            return []

    def create_domain(self, domain_name, id_thing=None, id_account=None, created_datetime=None, 
                     subtype=None, color=None, make=None, model=None, year=None, gps=None):
        """
        Crea un nuevo dominio con todos los campos disponibles.
        """
        try:
            if created_datetime is None:
                created_datetime = datetime.utcnow()
                
            new_domain = Domain(
                domain=domain_name, 
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
            self.session.add(new_domain)
            self.session.commit()
            print(f"✅ Domain creado con ID {new_domain.id}")
            return new_domain.to_dict()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al crear el domain: {e}")
            return None

    def update_domain_created_datetime(self, domain_id, created_datetime):
        """
        Actualiza el campo created_datetime de un dominio específico
        """
        try:
            domain = self.session.query(Domain).filter(Domain.id == domain_id).first()
            if domain:
                domain.created_datetime = created_datetime
                self.session.commit()
                print(f"✅ Fecha de creación actualizada para domain ID {domain_id}")
                return domain.to_dict()
            else:
                print(f"⚠️ No se encontró el domain con ID {domain_id}.")
                return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al actualizar created_datetime del domain: {e}")
            return None

    def update_domain_vehicle_fields(self, domain_id, subtype=None, color=None, make=None, 
                                   model=None, year=None, gps=None):
        """
        Actualiza los campos de vehículo de un domain específico.
        """
        try:
            domain = self.session.query(Domain).filter(Domain.id == domain_id).first()
            if domain:
                if subtype is not None:
                    domain.subtype = subtype
                if color is not None:
                    domain.color = color
                if make is not None:
                    domain.make = make
                if model is not None:
                    domain.model = model
                if year is not None:
                    domain.year = year
                if gps is not None:
                    domain.gps = gps
                    
                self.session.commit()
                print(f"✅ Campos de vehículo actualizados para domain ID {domain_id}")
                return domain.to_dict()
            else:
                print(f"⚠️ No se encontró el domain con ID {domain_id}.")
                return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al actualizar campos de vehículo del domain: {e}")
            return None

    def bulk_update_created_datetime_from_vehicle(self):
        """
        Actualiza created_datetime de domains donde sea NULL usando datos de strix.vvehicle
        """
        try:
            from sqlalchemy import text
            
            query = text("""
                UPDATE public."domain" AS d
                SET created_datetime = v.created_datetime
                FROM strix.vvehicle AS v
                WHERE d.id_thing = v.id
                  AND d.created_datetime IS NULL
                  AND v.created_datetime IS NOT NULL
            """)
            
            result = self.session.execute(query)
            self.session.commit()
            print(f"✅ Se actualizaron {result.rowcount} domains con created_datetime desde vvehicle")
            return result.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error en bulk update de created_datetime: {e}")
            return 0

    def bulk_update_vehicle_fields_from_vehicle(self):
        """
        Actualiza campos de vehículo de domains usando datos de strix.vvehicle
        """
        try:
            from sqlalchemy import text
            
            query = text("""
                UPDATE public."domain" AS d
                SET 
                    subtype = v.subtype,
                    color = v.color,
                    make = v.make,
                    model = v.model,
                    year = v.year,
                    gps = v.gps
                FROM strix.vvehicle AS v
                WHERE d.id_thing = v.id
                  AND (d.subtype IS NULL OR d.color IS NULL OR d.make IS NULL 
                       OR d.model IS NULL OR d.year IS NULL OR d.gps IS NULL)
            """)
            
            result = self.session.execute(query)
            self.session.commit()
            print(f"✅ Se actualizaron {result.rowcount} domains con campos de vehículo desde vvehicle")
            return result.rowcount
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error en bulk update de campos de vehículo: {e}")
            return 0

    def get_domains_by_vehicle_criteria(self, make=None, model=None, year=None, color=None):
        """
        Obtiene domains filtrados por criterios de vehículo.
        """
        try:
            query = self.session.query(Domain)
            
            if make is not None:
                query = query.filter(Domain.make == make)
            if model is not None:
                query = query.filter(Domain.model == model)
            if year is not None:
                query = query.filter(Domain.year == year)
            if color is not None:
                query = query.filter(Domain.color == color)
                
            domains = query.all()
            return [domain.to_dict() for domain in domains]
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener domains por criterios de vehículo: {e}")
            return []

    def get_domains_with_null_created_datetime(self):
        """
        Obtiene todos los dominios que tienen created_datetime = NULL
        """
        try:
            domains = self.session.query(Domain).filter(Domain.created_datetime.is_(None)).all()
            return [domain.to_dict() for domain in domains]
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener domains con created_datetime NULL: {e}")
            return []

    def delete_domain(self, domain_id):
        try:
            domain = self.session.query(Domain).filter(Domain.id == domain_id).first()
            if domain:
                self.session.delete(domain)
                self.session.commit()
                print(f"✅ Domain con ID {domain_id} eliminado correctamente.")
                return True
            else:
                print(f"⚠️ No se encontró el domain con ID {domain_id}.")
                return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al eliminar el domain con ID {domain_id}: {e}")
            return False

    def get_existing_domains_by_name_and_account(self):
        try:
            return self.session.query(Domain.domain, Domain.id_account).all()
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener dominios existentes: {e}")
            return []

    def get_existing_domains_by_names(self, domain_names: list):
        try:
            domains = self.session.query(Domain).filter(Domain.domain.in_(domain_names)).all()
            return [d.to_dict() for d in domains]
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener dominios por nombres: {e}")
            return []

    def bulk_insert_domains(self, domains_data):
        """
        Inserta múltiples domains en una sola operación.
        """
        try:
            self.session.bulk_insert_mappings(Domain, domains_data)
            self.session.commit()
            print(f"✅ {len(domains_data)} domains insertados correctamente.")
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error en bulk insert de domains: {e}")
            return False