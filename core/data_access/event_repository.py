from core.models.event import Event
from core.models.domain import Domain
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from sqlalchemy import tuple_
from datetime import datetime, timedelta
import pandas as pd
from core.utils.datetime_utils import to_timestamp_ms


class EventRepository:
    """
    Repositorio para manejar las operaciones CRUD de la tabla event.
    Requiere una sesión SQLAlchemy inyectada desde UnitOfWork.
    """

    def __init__(self, session):
        self.session = session

    def create_event(self, id_domain, latitude, longitude, speed, event, timestamp, odometer, heading):
        try:
            domain = self.session.query(Domain).filter(Domain.id == id_domain).first()
            if not domain:
                print(f"❌ Error: No existe el dominio con ID {id_domain}.")
                return None

            new_event = Event(
                id_domain=id_domain,
                latitude=latitude,
                longitude=longitude,
                speed=speed,
                event=event,
                timestamp=timestamp,
                odometer=odometer,
                heading=heading
            )
            self.session.add(new_event)
            self.session.commit()
            print(f"✅ Evento creado con ID {new_event.id}")
            return new_event.to_dict()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al crear el evento: {e}")
            return None

    def get_event_by_id(self, event_id):
        try:
            event = self.session.query(Event).filter(Event.id == event_id).first()
            return event.to_dict() if event else None
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener el evento con ID {event_id}: {e}")
            return None

    def get_events_by_domain(self, id_domain):
        try:
            events = self.session.query(Event).filter(Event.id_domain == id_domain).all()
            return [event.to_dict() for event in events] if events else []
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener eventos para el dominio con ID {id_domain}: {e}")
            return []

    def get_events_by_domain_and_date(self, id_domain, desde, hasta):
        try:
            # Usar función genérica
            desde_timestamp = to_timestamp_ms(desde)
            hasta_timestamp = to_timestamp_ms(hasta)
            print(f"Desde timestamp={desde_timestamp}, Hasta timestamp={hasta_timestamp}")
        except Exception as e:
            print(f"❌ Error al interpretar fechas: {e}")
            return []

        try:
            events = (self.session.query(Event)
                    .filter(Event.id_domain == id_domain,
                            Event.timestamp >= desde_timestamp,
                            Event.timestamp <= hasta_timestamp)
                    .order_by(Event.timestamp)
                    .all())
            return [event.to_dict() for event in events] if events else []
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener eventos en rango de fechas: {e}")
            return []

    def delete_event(self, event_id):
        try:
            event = self.session.query(Event).filter(Event.id == event_id).first()
            if not event:
                print(f"⚠️ No se encontró el evento con ID {event_id}.")
                return False

            self.session.delete(event)
            self.session.commit()
            print(f"✅ Evento con ID {event_id} eliminado.")
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al eliminar el evento con ID {event_id}: {e}")
            return False

    def store_events(self, events):
        try:
            event_keys = {(e["id_domain"], e["timestamp"]) for e in events}
            existing_events = self.session.query(Event.id_domain, Event.timestamp).filter(
                tuple_(Event.id_domain, Event.timestamp).in_(event_keys)
            ).all()
            existing_keys = {(e.id_domain, e.timestamp) for e in existing_events}
            new_events = [e for e in events if (e["id_domain"], e["timestamp"]) not in existing_keys]

            if new_events:
                self.session.bulk_insert_mappings(Event, new_events)
                self.session.commit()
                print(f"✅ {len(new_events)} eventos almacenados en la base de datos.")
            else:
                print("⚠ No hay eventos nuevos para almacenar.")
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al almacenar eventos: {e}")
