# reports/incident/services/geocode_service.py

from reports.incident.data_access.incident_repository import IncidentRepository
from reports.incident.adapters.geocoding_adapter import GeocodingAdapter


class GeocodeService:
    def __init__(self, uow):
        self.uow = uow
        self.adapter = GeocodingAdapter()

    def enrich_incidents_with_coordinates(self):
        with self.uow:
            repo = IncidentRepository(self.uow.session)
            pendientes = repo.get_pending_geocoding()

            if not pendientes:
                print("✅ No hay incidentes pendientes de geocodificación.")
                return

            updated = 0
            for row in pendientes:
                address = self._build_address(row)
                domain = row["domain"]
                fecha = row["fecha"]

                try:
                    lat, lon = self.adapter.geocode(
                        address,
                        domain=domain,
                        fecha=fecha,
                        disable_cache=False,
                        use_google=True,
                        use_osm=False,
                        use_opencage=False,
                        use_locationiq=False
                    )
                    if lat and lon:
                        repo.update_coordinates(row["id"], lat, lon)
                        updated += 1
                        print(f"✅ {domain} geocodificado en ({lat}, {lon})")
                except Exception as e:
                    print(f"❌ Error geocodificando {domain}: {str(e)}")

            self.uow.commit()
            print(f"🏁 Geocodificación finalizada. Total actualizados: {updated}")

    def _build_address(self, row):
        return f"{row['calle']}, {row['ciudad']}, {row['provincia']}"
