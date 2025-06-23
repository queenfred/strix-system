from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

class UserAccessRepository:
    def __init__(self, session):
        self.session = session

    def assign_role_to_user(self, user_id, role_id):
        try:
            self.session.execute(
                text("""
                    INSERT INTO public.user_roles (user_id, role_id)
                    VALUES (:user_id, :role_id)
                    ON CONFLICT DO NOTHING
                """),
                {"user_id": user_id, "role_id": role_id}
            )
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al asignar rol a usuario: {e}")
            return False

    def assign_permission_to_user(self, user_id, permission_id):
        try:
            self.session.execute(
                text("""
                    INSERT INTO public.user_permissions (user_id, permission_id)
                    VALUES (:user_id, :permission_id)
                    ON CONFLICT DO NOTHING
                """),
                {"user_id": user_id, "permission_id": permission_id}
            )
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al asignar permiso a usuario: {e}")
            return False

    def assign_permission_to_role(self, role_id, permission_id):
        try:
            self.session.execute(
                text("""
                    INSERT INTO public.role_permissions (role_id, permission_id)
                    VALUES (:role_id, :permission_id)
                    ON CONFLICT DO NOTHING
                """),
                {"role_id": role_id, "permission_id": permission_id}
            )
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al asignar permiso a rol: {e}")
            return False

    def user_has_permission(self, user_id, permission_name):
        result = self.session.execute(text("""
            SELECT 1
            FROM public.user_permissions up
            JOIN public.permissions p ON up.permission_id = p.id
            WHERE up.user_id = :user_id AND p.name = :permission_name
            UNION
            SELECT 1
            FROM public.user_roles ur
            JOIN public.role_permissions rp ON ur.role_id = rp.role_id
            JOIN public.permissions p ON rp.permission_id = p.id
            WHERE ur.user_id = :user_id AND p.name = :permission_name
            LIMIT 1
        """), {"user_id": user_id, "permission_name": permission_name}).fetchone()

        return result is not None
