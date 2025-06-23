from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork

class RoleService:
    """
    Servicio para manejar operaciones CRUD de roles.
    """

    def create_role(self, name, description=None, uow=None):
        if uow is not None:
            return uow.roles.create_role(name, description)
        with SQLAlchemyUnitOfWork() as uow:
            return self.create_role(name, description, uow=uow)
        
    def get_or_create_role(self, name, description=None, uow=None):
        if uow is not None:
            existing = uow.roles.get_role_by_name(name)
            if existing:
                return existing
            return uow.roles.create_role(name, description)

        with SQLAlchemyUnitOfWork() as uow:
            return self.get_or_create_role(name, description, uow=uow)


    def get_role_by_name(self, name, uow=None):
        if uow is not None:
            return uow.roles.get_role_by_name(name)
        with SQLAlchemyUnitOfWork() as uow:
            return self.get_role_by_name(name, uow=uow)

    def get_role_by_id(self, role_id, uow=None):
        if uow is not None:
            return uow.roles.get_role_by_id(role_id)
        with SQLAlchemyUnitOfWork() as uow:
            return self.get_role_by_id(role_id, uow=uow)

    def get_all_roles(self, uow=None):
        if uow is not None:
            return uow.roles.get_all_roles()
        with SQLAlchemyUnitOfWork() as uow:
            return self.get_all_roles(uow=uow)

    def update_role(self, role_id, name=None, description=None, uow=None):
        if uow is not None:
            return uow.roles.update_role(role_id, name, description)
        with SQLAlchemyUnitOfWork() as uow:
            return self.update_role(role_id, name, description, uow=uow)

    def delete_role(self, role_id, uow=None):
        if uow is not None:
            return uow.roles.delete_role(role_id)
        with SQLAlchemyUnitOfWork() as uow:
            return self.delete_role(role_id, uow=uow)
