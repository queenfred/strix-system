
import pandas as pd
from core.services.domain_service import DomainService
from reports.incident.data_access.incident_repository import IncidentRepository
from datetime import datetime


class IncidentService:
    def __init__(self, uow):
        self.uow = uow
        self.domain_service = DomainService()
    
    def get_all_incidents(self):
        with self.uow:
            repo = self.uow.incidents
            rows = repo.get_all_incidents()
            return rows  # Devuelve lista de dicts

    def ingest_and_save_incidents(self, file):
        df = pd.read_excel(file, sheet_name="Hoja1")

        # Normalizar nombres de columnas a minúsculas sin espacios
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        # Mapeo flexible de nombres esperados
        col_map = {
            "patente_del_vehículo_del_asegurado": "domain",
            "fecha_y_hora_de_ocurrencia_del_siniestro": "fecha_ocurrencia",
            "fecha": "fecha_ocurrencia",
            "calle_de_ocurrencia": "calle",
            "calle": "calle",
            "ciudad_de_ocurrencia": "ciudad",
            "ciudad": "ciudad",
            "provincia_de_ocurrencia": "provincia",
            "provincia": "provincia"
        }

        df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})
        required_cols = ["domain", "fecha_ocurrencia"]

        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"❌ Falta la columna requerida: '{col}'")

        df["domain"] = df["domain"].str.replace(" ", "", regex=False)
        df["fecha_ocurrencia"] = pd.to_datetime(df["fecha_ocurrencia"], errors="coerce", dayfirst=True)
        df = df.dropna(subset=["fecha_ocurrencia"])

        domain_names = df["domain"].unique().tolist()
        existing_domains = self.domain_service.get_existing_domains_by_names(domain_names)

        if not existing_domains:
            raise ValueError("❌ No se encontraron dominios existentes para procesar.")

        # Transformar lista de dicts a DataFrame
        df_valid = pd.DataFrame([{
            "id": d["id"],
            "domain": d["domain"],
            "id_account": d["id_account"]
        } for d in existing_domains])

        valid_domains = df_valid["domain"].tolist()
        df_filtered = df[df["domain"].isin(valid_domains)]
        df_filtered = df_filtered.merge(df_valid, on="domain", how="left")

        with self.uow:
            repo = IncidentRepository(self.uow.session)
            for _, row in df_filtered.iterrows():
                repo.save_incident({
                    "id_domain": int(row["id"]),
                    "domain": row["domain"],
                    "fecha_ocurrencia": row["fecha_ocurrencia"],
                    "calle": row.get("calle"),
                    "ciudad": row.get("ciudad"),
                    "provincia": row.get("provincia"),
                    "latitud": None,
                    "longitud": None,
                    "distancia_circulacion": None,
                    "fecha_circulacion": None,
                    "hora_circulacion": None,
                    "parada_zona": None,
                    "latitud_parada_zona": None,
                    "longitud_parada_zona": None,
                    "clasificacion": None,
                    "created_at": datetime.now()
                })
            self.uow.commit()

        return df_filtered.reset_index(drop=True)
