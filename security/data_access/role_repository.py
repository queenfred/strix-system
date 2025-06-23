from security.models.role import Role
from sqlalchemy.exc import SQLAlchemyError


class RoleRepository:
    def __init__(self, session):
        self.session = session

    def create_role(self, name, description=None):
        try:
            role = Role(name=name, description=description)
            self.session.add(role)
            self.session.commit()
            return role.to_dict()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al crear rol: {e}")
            return None

    def get_role_by_name(self, name):
        try:
            role = self.session.query(Role).filter_by(name=name).first()
            return role.to_dict() if role else None
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener rol por nombre: {e}")
            return None

    def get_role_by_id(self, role_id):
        try:
            role = self.session.query(Role).filter_by(id=role_id).first()
            return role.to_dict() if role else None
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener rol por ID: {e}")
            return None

    def get_all_roles(self):
        try:
            roles = self.session.query(Role).all()
            return [r.to_dict() for r in roles]
        except SQLAlchemyError as e:
            print(f"❌ Error al listar roles: {e}")
            return []

    def update_role(self, role_id, name=None, description=None):
        try:
            role = self.session.query(Role).filter_by(id=role_id).first()
            if not role:
                return None
            if name:
                role.name = name
            if description:
                role.description = description
            self.session.commit()
            return role.to_dict()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al actualizar rol: {e}")
            return None

    def delete_role(self, role_id):
        try:
            role = self.session.query(Role).filter_by(id=role_id).first()
            if not role:
                return False
            self.session.delete(role)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al eliminar rol: {e}")
            return False
