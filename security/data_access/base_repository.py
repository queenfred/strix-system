from sqlalchemy.exc import SQLAlchemyError

class BaseRepository:
    def __init__(self, session, model):
        self.session = session
        self.model = model

    def get_by_id(self, obj_id):
        try:
            result = self.session.query(self.model).filter_by(id=obj_id).first()
            return result.to_dict() if result else None
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener por ID: {e}")
            return None

    def get_all(self):
        try:
            results = self.session.query(self.model).all()
            return [r.to_dict() for r in results]
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener todos: {e}")
            return []

    def create(self, **kwargs):
        try:
            obj = self.model(**kwargs)
            self.session.add(obj)
            self.session.commit()
            return obj.to_dict()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al crear objeto: {e}")
            return None

    def update(self, obj_id, **kwargs):
        try:
            obj = self.session.query(self.model).filter_by(id=obj_id).first()
            if not obj:
                return None
            for key, value in kwargs.items():
                setattr(obj, key, value)
            self.session.commit()
            return obj.to_dict()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al actualizar objeto: {e}")
            return None

    def delete(self, obj_id):
        try:
            obj = self.session.query(self.model).filter_by(id=obj_id).first()
            if not obj:
                return False
            self.session.delete(obj)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al eliminar objeto: {e}")
            return False
