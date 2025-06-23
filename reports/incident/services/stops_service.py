# reports/incident/services/stops_service.py

import pandas as pd
from reports.incident.adapters.stops_adapter import StopsAdapter


class StopsService:
    @staticmethod
    def compute_stop(row: pd.Series, recorrido_df: pd.DataFrame) -> pd.Series:
        domain = str(row["domain"]).strip().lower()
        ref_point = (row["latitud"], row["longitud"])

        # Filtrar solo eventos del dominio actual
        recorrido_df = recorrido_df[recorrido_df["domain"].str.strip().str.lower() == domain]
        if recorrido_df.empty:
            print(f"⚠️ No hay recorrido para parada: {domain}")
            return pd.Series({
                "parada_zona": 0,
                "latitud_parada_zona": None,
                "longitud_parada_zona": None
            })

        # Usar el adapter para detectar la parada más larga
        try:
            duracion, lat_parada, lon_parada = StopsAdapter.detect_stop(
                recorrido_df,
                reference_point=ref_point,
                search_radius=500,
                min_stop=10,
                max_stop=36000
            )

            return pd.Series({
                "parada_zona": duracion,
                "latitud_parada_zona": lat_parada,
                "longitud_parada_zona": lon_parada
            })
        except Exception as e:
            print(f"❌ Error en cálculo de parada para {domain}: {str(e)}")
            return pd.Series({
                "parada_zona": 0,
                "latitud_parada_zona": None,
                "longitud_parada_zona": None
            })

