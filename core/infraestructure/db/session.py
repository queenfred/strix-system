# core/infraestructure/db/session.py
from sqlalchemy.orm import sessionmaker, scoped_session
from core.infraestructure.db.postgres import Postgres

class SessionFactory:
    _engine = None
    _Session = None

    @classmethod
    def initialize(cls):
        if cls._engine is None:
            db = Postgres()  # 👈 Siempre la misma instancia
            cls._engine = db.connPostgres()
            cls._Session = scoped_session(sessionmaker(bind=cls._engine))

    @classmethod
    def get_session(cls):
        if cls._Session is None:
            cls.initialize()
        return cls._Session()


