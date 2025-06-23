from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork

class PermissionService:
    """
    Servicio para gestionar permisos en el sistema.
    """

    def create_permission(self, name, description=None, uow=None):
        if uow is not None:
            return uow.permissions.create(name=name, description=description)
        with SQLAlchemyUnitOfWork() as uow:
            return self.create_permission(name, description, uow=uow)

    def get_permission_by_name(self, name, uow=None):
        if uow is not None:
            return uow.permissions.get_permission_by_name(name)
        with SQLAlchemyUnitOfWork() as uow:
            return self.get_permission_by_name(name, uow=uow)

    def get_or_create_permission(self, name, description=None, uow=None):
        if uow is not None:
            existing = uow.permissions.get_permission_by_name(name)
            if existing:
                return existing
            return uow.permissions.create(name=name, description=description)
        with SQLAlchemyUnitOfWork() as uow:
            return self.get_or_create_permission(name, description, uow=uow)

    def get_permission_by_id(self, permission_id, uow=None):
        if uow is not None:
            return uow.permissions.get_by_id(permission_id)
        with SQLAlchemyUnitOfWork() as uow:
            return self.get_permission_by_id(permission_id, uow=uow)

    def get_all_permissions(self, uow=None):
        if uow is not None:
            return uow.permissions.get_all()
        with SQLAlchemyUnitOfWork() as uow:
            return self.get_all_permissions(uow=uow)

    def update_permission(self, permission_id, **kwargs):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.permissions.update(permission_id, **kwargs)

    def delete_permission(self, permission_id):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.permissions.delete(permission_id)