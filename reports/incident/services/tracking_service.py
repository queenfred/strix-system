# report/incident/services/tracking_service.py

from sqlalchemy import text
import pandas as pd

from reports.incident.data_access.incident_repository import IncidentRepository

from .domain_tracking_service import DomainTrackingService

from .distance_service import DistanceService
from .stops_service import StopsService


class TrackingService:
    def __init__(self, uow):
        self.uow = uow
        self.domain_tracker = DomainTrackingService(uow)

    def enrich_with_tracking_data(self):
        with self.uow:
            repo = IncidentRepository(self.uow.session)
            incidents = repo.get_incidents_pending_tracking()#ok

            if not incidents:
                print("✅ No hay incidentes pendientes de tracking.")
                return

            updated_count = 0
            for data in incidents:
                id_ = data["id"]
                id_domain = data["id_domain"]
                domain = data["domain"]
                fecha = pd.to_datetime(data["fecha_ocurrencia"])

                recorrido_df = self.domain_tracker.get_events_by_domain_and_date(id_domain, fecha, domain)

                if recorrido_df is None or recorrido_df.empty:
                    continue

                dist_info = DistanceService.compute_min_distance(pd.Series(data), recorrido_df)
                stop_info = StopsService.compute_stop(pd.Series(data), recorrido_df)

                tracking_info = {**dist_info, **stop_info}
                repo.update_tracking_data(id_, tracking_info)
                updated_count += 1

            self.uow.commit()
            print(f"✅ Se actualizaron {updated_count} incidentes con datos de tracking.")