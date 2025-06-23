from core.models.domain import Domain
from sqlalchemy.exc import SQLAlchemyError

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

    def create_domain(self, domain_name, id_thing=None, id_account=None):
        try:
            new_domain = Domain(domain=domain_name, id_thing=id_thing, id_account=id_account)
            self.session.add(new_domain)
            self.session.commit()
            print(f"✅ Domain creado con ID {new_domain.id}")
            return new_domain.to_dict()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al crear el domain: {e}")
            return None

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