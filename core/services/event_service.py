from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork

class EventService:
    """
    Servicio para manejar eventos a través del repositorio EventRepository.
    """

    def __init__(self, uow):
        self.uow = uow

    def get_event_by_id(self, event_id):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.events.get_event_by_id(event_id)

    def get_events_by_domain(self, id_domain):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.events.get_events_by_domain(id_domain)

    def get_events_by_domain_and_date(self, id_domain, desde, hasta):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.events.get_events_by_domain_and_date(id_domain, desde, hasta)

    def create_event(self, id_domain, latitude, longitude, speed, event, timestamp, odometer, heading):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.events.create_event(id_domain, latitude, longitude, speed, event, timestamp, odometer, heading)

    def delete_event(self, event_id):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.events.delete_event(event_id)

    def store_events(self, events):
        with SQLAlchemyUnitOfWork() as uow:
            return uow.events.store_events(events)
