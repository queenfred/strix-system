from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork

class AccessControlService:

    def create_role(self, name, description=None, uow=None):
        if uow is not None:
            existing = uow.roles.get_role_by_name(name)
            if existing:
                return existing
            role = uow.roles.create_role(name, description)
            uow.commit()
            return role

        with SQLAlchemyUnitOfWork() as uow_local:
            return self.create_role(name, description, uow=uow_local)

    def create_permission(self, name, description=None, uow=None):
        if uow is not None:
            permission = uow.permissions.create_permission(name, description)
            uow.commit()
            return permission

        with SQLAlchemyUnitOfWork() as uow_local:
            return self.create_permission(name, description, uow=uow_local)

    def get_or_create_permission(self, name, description=None, uow=None):
        if uow is not None:
            existing = uow.permissions.get_permission_by_name(name)
            if existing:
                return existing
            permission = uow.permissions.create_permission(name, description)
            uow.commit()
            return permission

        with SQLAlchemyUnitOfWork() as uow_local:
            return self.get_or_create_permission(name, description, uow=uow_local)

    def get_or_create_role(self, name, description=None, uow=None):
        if uow is not None:
            existing = uow.roles.get_role_by_name(name)
            if existing:
                return existing
            role = uow.roles.create_role(name, description)
            uow.commit()
            return role

        with SQLAlchemyUnitOfWork() as uow_local:
            return self.get_or_create_role(name, description, uow=uow_local)

    def assign_permission_to_role(self, role_id, permission_id, uow=None):
        if uow is not None:
            result = uow.user_access.assign_permission_to_role(role_id, permission_id)
            uow.commit()
            return result

        with SQLAlchemyUnitOfWork() as uow_local:
            return self.assign_permission_to_role(role_id, permission_id, uow=uow_local)

    def assign_role_to_user(self, user_id, role_id, uow=None):
        if uow is not None:
            result = uow.user_access.assign_role_to_user(user_id, role_id)
            uow.commit()
            return result

        with SQLAlchemyUnitOfWork() as uow_local:
            return self.assign_role_to_user(user_id, role_id, uow=uow_local)

