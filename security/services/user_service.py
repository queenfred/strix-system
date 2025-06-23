from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from security.utils.password_utils import hash_password, verify_password
from sqlalchemy.exc import IntegrityError

class UserService:

    def register_user(self, username, email, password, full_name=None, uow=None):
        hashed = hash_password(password)

        if uow is not None:
            if uow.users.get_user_by_username(username):
                print(f"⚠️ Usuario '{username}' ya existe.")
                return None
            if uow.users.get_user_by_email(email):
                print(f"⚠️ Email '{email}' ya está en uso.")
                return None

            try:
                user = uow.users.create_user(username, email, hashed, full_name)
                uow.commit()
                return user
            except IntegrityError:
                uow.rollback()
                print("❌ Error de integridad al registrar el usuario.")
                return None

        with SQLAlchemyUnitOfWork() as uow_local:
            return self.register_user(username, email, password, full_name, uow=uow_local)

    def authenticate(self, username, password, uow=None):
        if uow is not None:
            return uow.users.validate_user_credentials(username, password)

        with SQLAlchemyUnitOfWork() as uow_local:
            return self.authenticate(username, password, uow=uow_local)

    def get_user(self, username, uow=None):
        if uow is not None:
            return uow.users.get_user_by_username(username)

        with SQLAlchemyUnitOfWork() as uow_local:
            return self.get_user(username, uow=uow_local)

    def list_users(self, uow=None):
        if uow is not None:
            return uow.users.get_all_users()

        with SQLAlchemyUnitOfWork() as uow_local:
            return self.list_users(uow=uow_local)

    def deactivate(self, user_id, uow=None):
        if uow is not None:
            result = uow.users.deactivate_user(user_id)
            uow.commit()
            return result

        with SQLAlchemyUnitOfWork() as uow_local:
            return self.deactivate(user_id, uow=uow_local)


    def get_user_by_email(self, email, uow=None):
        if uow is not None:
            return uow.users.get_user_by_email(email)

        with SQLAlchemyUnitOfWork() as uow_local:
            return self.get_user_by_email(email, uow=uow_local)