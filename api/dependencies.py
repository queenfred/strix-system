from fastapi import Depends
from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork

# Esto permite que cada request tenga su propio contexto de UoW, gestionando correctamente la sesión, commit y rollback.
def get_uow():
    with SQLAlchemyUnitOfWork() as uow:
        yield uow
