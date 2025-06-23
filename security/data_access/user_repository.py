from security.models.user import User
from security.data_access.base_repository import BaseRepository
from sqlalchemy.exc import IntegrityError
from security.utils.password_utils import verify_password

class UserRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, User)

    def create_user(self, username, email, password, full_name=None):
        try:
            new_user = User(username=username, email=email, full_name=full_name, password=password)
            self.session.add(new_user)
            self.session.flush()  # Para obtener el ID si es necesario
            return new_user.to_dict()
        except IntegrityError as e:
            if 'duplicate key value violates unique constraint' in str(e.orig):
                print(f"⚠️ El usuario '{username}' ya existe.")
                return None
            raise e

    def get_user_by_username(self, username):
        user = self.session.query(User).filter_by(username=username).first()
        return user.to_dict() if user else None

    def get_user_by_email(self, email):
        user = self.session.query(User).filter_by(email=email).first()
        return user.to_dict() if user else None

    def get_all_users(self):
        users = self.session.query(User).all()
        return [user.to_dict() for user in users]

    def deactivate_user(self, user_id):
        user = self.session.get(User, user_id)
        if user:
            user.is_active = False
            return user.to_dict()
        return None

    def validate_user_credentials(self, username, raw_password):
        user = self.session.query(User).filter_by(username=username).first()
        if user and verify_password(raw_password, user.password):
            return {
                "user": user.to_dict(),
                "roles": [
                    {
                        "id": role.id,
                        "name": role.name,
                        "permissions": [
                            {"id": perm.id, "name": perm.name}
                            for perm in role.permissions
                        ]
                    }
                    for role in user.roles
                ]
            }
        return None

