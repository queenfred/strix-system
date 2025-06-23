from security.models.permission import Permission
from security.data_access.base_repository import BaseRepository

class PermissionRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Permission)

    def get_permission_by_name(self, name):
        try:
            result = self.session.query(Permission).filter_by(name=name).first()
            return result.to_dict() if result else None
        except Exception as e:
            print(f"❌ Error al obtener permiso por nombre: {e}")
            return None
