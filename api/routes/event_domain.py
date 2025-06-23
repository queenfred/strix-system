# routes/event_domain_router.py

from fastapi import APIRouter, Query
from datetime import datetime
from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from core.services.event_domain_service import EventDomainService


router = APIRouter(prefix="/event_domain", tags=["Event Domain"])

@router.get("/event-domain/get-or-process-events")
def get_or_process_events(
    id_domain: int = Query(..., description="ID del dominio"),
    desde: datetime = Query(..., description="Fecha inicial (formato ISO, ejemplo: 2024-11-17T04:59:10)"),
    hasta: datetime = Query(..., description="Fecha final (formato ISO, ejemplo: 2024-11-18T04:59:10)")
):
    """
    Busca eventos de un dominio en la base de datos o los procesa si no existen.
    """
    uow = SQLAlchemyUnitOfWork()
    service = EventDomainService(uow)

    eventos = service.get_or_process_events(id_domain, desde, hasta)

    return {"domain_id": id_domain, "eventos": eventos}
