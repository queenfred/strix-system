# data_access/repositories/incident_repository.py

from sqlalchemy import text
from datetime import datetime
import math
import pandas as pd

class IncidentRepository:
    def __init__(self, session):
        self.session = session

    def get_all_incidents(self):
        """
        Recupera todos los incidentes verificados.
        """
        query = text("SELECT * FROM public.incidentes_verificados")
        result = self.session.execute(query)
        return [dict(row._mapping) for row in result]

    def get_by_domain(self, domain: str):
        """
        Recupera incidentes por dominio.
        """
        query = text("""
            SELECT * FROM public.incidentes_verificados
            WHERE domain = :domain
        """)
        result = self.session.execute(query, {"domain": domain})
        return [dict(row._mapping) for row in result]


    def incident_exists(self, domain: str, fecha_ocurrencia: datetime) -> bool:
        """
        Verifica si ya existe un incidente con el mismo dominio y fecha.
        """
        query = text("""
            SELECT id FROM public.incidentes_verificados
            WHERE domain = :domain AND fecha_ocurrencia = :fecha_ocurrencia
        """)
        result = self.session.execute(query, {
            "domain": domain,
            "fecha_ocurrencia": fecha_ocurrencia
        }).fetchone()
        return result is not None

    def save_incident(self, incident_data: dict):
        """
        Inserta un incidente verificado solo si no existe uno con el mismo dominio y fecha.
        """
        # Validar existencia previa
        if self.incident_exists(incident_data["domain"], incident_data["fecha_ocurrencia"]):
            print(f"⚠️ Incidente ya existe para dominio {incident_data['domain']} en {incident_data['fecha_ocurrencia']}")
            return

        # Insertar si no existe
        insert_query = text("""
            INSERT INTO public.incidentes_verificados (
                id_domain,
                domain,
                fecha_ocurrencia,
                calle,
                ciudad,
                provincia,
                latitud,
                longitud,
                distancia_circulacion,
                fecha_circulacion,
                hora_circulacion,
                parada_zona,
                latitud_parada_zona,
                longitud_parada_zona,
                clasificacion,
                created_at
            ) VALUES (
                :id_domain,
                :domain,
                :fecha_ocurrencia,
                :calle,
                :ciudad,
                :provincia,
                :latitud,
                :longitud,
                :distancia_circulacion,
                :fecha_circulacion,
                :hora_circulacion,
                :parada_zona,
                :latitud_parada_zona,
                :longitud_parada_zona,
                :clasificacion,
                :created_at
            )
        """)

        self.session.execute(insert_query, {
            **incident_data,
            "created_at": incident_data.get("created_at") or datetime.now()
        })




##### incident_geocode_repository

    def get_pending_geocoding(self):
        result = self.session.execute(text("""
            SELECT id, calle, ciudad, provincia, 
                fecha_ocurrencia AS fecha,
                domain
            FROM public.incidentes_verificados
            WHERE latitud IS NULL OR longitud IS NULL
        """))
        return [dict(row._mapping) for row in result]


    def update_coordinates(self, incident_id, lat, lon):
        try:
            self.session.execute(text("""
                UPDATE public.incidentes_verificados
                SET latitud = :lat, longitud = :lon
                WHERE id = :id
            """), {
                "lat": float(lat),
                "lon": float(lon),
                "id": incident_id
            })
        except Exception as e:
            self.session.rollback()
            print(f"❌ Error al actualizar coordenadas para incidente ID {incident_id}: {e}")




######Tracking Service
    def update_tracking_data(self, incident_id, tracking_info: dict):
        try:
            # Convertir correctamente los valores a tipos nativos
            def safe_float(val):
                return float(val) if val is not None and not pd.isna(val) else None

            self.session.execute(text("""
                UPDATE public.incidentes_verificados
                SET distancia_circulacion = :distancia,
                    fecha_circulacion = :fecha_circulacion,
                    hora_circulacion = :hora_circulacion,
                    parada_zona = :parada_zona,
                    latitud_parada_zona = :lat_parada,
                    longitud_parada_zona = :lon_parada
                WHERE id = :id
            """), {
                "distancia": safe_float(tracking_info.get("distancia_circulacion")),
                "fecha_circulacion": tracking_info.get("fecha"),
                "hora_circulacion": tracking_info.get("hora"),
                "parada_zona": safe_float(tracking_info.get("parada_zona")),
                "lat_parada": safe_float(tracking_info.get("latitud_parada_zona")),
                "lon_parada": safe_float(tracking_info.get("longitud_parada_zona")),
                "id": incident_id
            })
        except Exception as e:
            self.session.rollback()
            print(f"❌ Error al actualizar tracking para incidente ID {incident_id}: {e}")

    def get_incidents_pending_tracking(self):
        query = text("""
            SELECT id,id_domain, domain, fecha_ocurrencia, latitud, longitud
            FROM public.incidentes_verificados
            WHERE latitud IS NOT NULL AND longitud IS NOT NULL
            AND distancia_circulacion IS NULL
        """)
        result = self.session.execute(query)
        return [dict(row._mapping) for row in result]

    #####

    def get_incidents_pending_classification(self):
            """
            Retorna los incidentes con distancia y parada cargadas pero sin clasificación.
            """
            """ Antes
                SELECT id, distancia_circulacion, parada_zona
                FROM public.incidentes_verificados
                WHERE distancia_circulacion IS NOT NULL
                AND parada_zona IS NOT NULL
                AND clasificacion IS NULL
            """
            query = text("""
                SELECT id, distancia_circulacion, parada_zona
                FROM public.incidentes_verificados
                WHERE clasificacion IS NULL
            """)
            result = self.session.execute(query)
            return [dict(row._mapping) for row in result]

    def update_classification(self, incident_id: int, clasificacion: str):
        try:
            self.session.execute(text("""
                UPDATE public.incidentes_verificados
                SET clasificacion = :clasificacion
                WHERE id = :id
            """), {"clasificacion": clasificacion, "id": incident_id})
        except Exception as e:
            self.session.rollback()
            print(f"❌ Error al clasificar incidente ID {incident_id}: {e}")