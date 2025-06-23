# report/incident/services/domain_tracking_service.py

import pandas as pd
from datetime import timedelta
from core.services.event_service import EventService


class DomainTrackingService:
    def __init__(self, uow):
        self.uow = uow
        self.event_service = EventService(uow)


    def get_events_by_domain_and_date(self, id_domain: int, incident_date: pd.Timestamp, domain: str = None) -> pd.DataFrame:
        if not isinstance(incident_date, pd.Timestamp):
            print(f"❌ Fecha inválida para el dominio: {domain or id_domain}")
            return None

        start_date = incident_date.normalize()
        end_date = start_date + timedelta(days=1) - timedelta(seconds=1)

        print(f"🔍 Obteniendo eventos para dominio ID {id_domain} - {start_date.date()} - {end_date.date()} ")

        #ACA 

        raw_events = self.event_service.get_events_by_domain_and_date(
            id_domain=id_domain,
            desde=start_date,
            hasta=end_date
        )

        if not raw_events:
            print(f"❌ No se encontraron eventos para id_domain {id_domain}")
            return None

        df = pd.DataFrame(raw_events)
        if domain:
            df["domain"] = domain
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", origin="unix")
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC").dt.tz_convert("America/Argentina/Buenos_Aires")

        columns = ["domain", "event", "latitude", "longitude", "timestamp", "odometer", "heading", "speed"]
        df = df.reindex(columns=[c for c in columns if c in df.columns])
        df = df.sort_values("timestamp")

        if (df["speed"] == 0).all():
            print(f"⚠️ Todos los eventos tienen velocidad cero para id_domain {id_domain}")
            return None

        return df
