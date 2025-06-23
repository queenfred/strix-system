# core/services/event_domain_service.py

from core.services.event_service import EventService
from core.services.domain_service import DomainService

class EventDomainService:
    """
    Servicio que maneja la recuperación o procesamiento de eventos según existencia.
    """
    def __init__(self, uow):
        self.uow = uow
        self.event_service = EventService(uow)
        self.domain_service = DomainService() 

    def get_or_process_events(self, id_domain, desde, hasta):
        """
        Retorna eventos de la base de datos. Si no existen, procesa eventos usando DomainService.
        """
        with self.uow:
            eventos = self.event_service.get_events_by_domain_and_date(id_domain, desde, hasta)

            if not eventos:
                print(f"⚠️ No se encontraron eventos en la DB para {id_domain}. Procesando...")
                self.domain_service.process_domain_id_events(id_domain, desde, hasta)

                # Reintentar después del procesamiento
                eventos = self.event_service.get_events_by_domain_and_date(id_domain, desde, hasta)
                
                if not eventos:
                    print(f"❌ No se pudieron obtener eventos luego del procesamiento para {id_domain}.")
            
            return eventos

