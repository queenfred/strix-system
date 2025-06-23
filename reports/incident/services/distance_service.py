# report/incident/services/distance_service.py

import pandas as pd
import numpy as np
from geopy.distance import geodesic


class DistanceService:
    @staticmethod
    def compute_min_distance(row: pd.Series, recorrido_df: pd.DataFrame) -> pd.Series:
        domain = str(row["domain"]).strip().lower()
        incident_date = pd.to_datetime(row["fecha_ocurrencia"]).date()
        geocode_point = (row["latitud"], row["longitud"])

        if pd.isna(geocode_point[0]) or pd.isna(geocode_point[1]):
            print(f"⚠️ Coordenadas inválidas para {domain}")
            return pd.Series({"distancia_circulacion": np.nan, "fecha": np.nan, "hora": np.nan})

        recorrido_df = recorrido_df[recorrido_df["domain"].str.strip().str.lower() == domain]
        recorrido_df = recorrido_df[pd.to_datetime(recorrido_df["timestamp"]).dt.date == incident_date]
        recorrido_df = recorrido_df.dropna(subset=["latitude", "longitude"])

        if recorrido_df.empty:
            print(f"⚠️ No hay eventos para {domain} en {incident_date}")
            return pd.Series({"distancia_circulacion": np.nan, "fecha": np.nan, "hora": np.nan})

        results = []
        for _, r in recorrido_df.iterrows():
            try:
                d = geodesic(geocode_point, (r["latitude"], r["longitude"])).kilometers
                ts = pd.to_datetime(r["timestamp"])
                results.append((d, ts))
            except Exception as e:
                print(f"Error calculando distancia: {e}")

        if results:
            min_d, ts = min(results, key=lambda x: x[0])
            return pd.Series({
                "distancia_circulacion": min_d,
                "fecha": ts.date() if pd.notnull(ts) else np.nan,
                "hora": ts.strftime("%H:%M:%S") if pd.notnull(ts) else np.nan
            })

        return pd.Series({"distancia_circulacion": np.nan, "fecha": np.nan, "hora": np.nan})
