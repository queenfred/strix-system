
import pandas as pd
from security.services.health_check import health_check

from core.services.domain_service import DomainService
from core.services.portfolio_service import PortfolioService
from core.services.vehicle_service import VehicleService
from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

class SiniestroProcessorService:
    """
    Pipeline que:
    1. Carga el archivo CSV con dominios y fechas.
    2. Chequea conexiones a PostgreSQL y S3.
    3. Busca los dominios en strix.vehicle.
    4. Almacena coincidencias en public.domain.
    5. Crea un nuevo portfolio con estos dominios.
    6. Ejecuta process_portfolio_events() en base a la fecha del siniestro.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.domain_service = DomainService()
        self.portfolio_service = PortfolioService()

    def run_pipeline(self):
        print("🔍 Verificando conexiones...")
        try:
            status = health_check()
            if not status.get("postgres") or not status.get("s3"):
                print("❌ Error en las conexiones. Abortando proceso.")
                return {"success": False, "message": "Fallo en conexión a PostgreSQL o S3."}
            print("✅ Conexiones correctas.")
        except Exception as e:
            print(f"❌ Error en el chequeo de conexiones: {e}")
            return {"success": False, "message": str(e)}

        try:
            print("📥 Cargando datos del archivo CSV...")
            df = pd.read_csv(self.file_path, encoding="utf-8")
            df["Domain"] = df["Domain"].astype(str).str.strip()
            df["Fecha y hora de ocurrencia del siniestro"] = pd.to_datetime(
                df["Fecha y hora de ocurrencia del siniestro"], dayfirst=True)
        except Exception as e:
            print(f"❌ Error al cargar o procesar el CSV: {e}")
            return {"success": False, "message": str(e)}

        try:
            domain_list = df["Domain"].tolist()
            print(f"🔎 Buscando {len(domain_list)} dominios en strix.vehicle...")
            with SQLAlchemyUnitOfWork() as uow:
                VehicleService(uow).create_domains_from_vehicles(domains=domain_list)
        except SQLAlchemyError as e:
            print(f"❌ Error al crear dominios desde vehicle: {e}")
            return {"success": False, "message": str(e)}

        try:
            print("🔄 Resolviendo nombres de dominio a IDs reales...")
            with SQLAlchemyUnitOfWork() as uow:
                existing_domains = uow.domains.get_domains_by_names(domain_list)
                domain_name_to_id = {d.domain: d.id for d in existing_domains}
                valid_domain_ids = list(domain_name_to_id.values())
                print(f"✅ Se encontraron {len(valid_domain_ids)} dominios válidos con ID.")
        except Exception as e:
            print(f"❌ Error al resolver dominios existentes: {e}")
            return {"success": False, "message": str(e)}

        try:
            print("📂 Creando un nuevo portfolio con estos dominios...")
            portfolio_id = self.portfolio_service.create_portfolio_with_domains(
                "Siniestro Pipeline Portfolio", valid_domain_ids)
            if not portfolio_id:
                print("❌ Error al crear el portfolio. Abortando proceso.")
                return {"success": False, "message": "No se pudo crear el portfolio."}
            print(f"✅ Portfolio {portfolio_id} creado exitosamente.")
        except SQLAlchemyError as e:
            print(f"❌ Error al crear el portfolio con dominios: {e}")
            return {"success": False, "message": str(e)}

        try:
            df_valid = df[df["Domain"].isin(domain_name_to_id.keys())].copy()
            df_valid["domain_id"] = df_valid["Domain"].map(domain_name_to_id)
        except Exception as e:
            print(f"❌ Error al preparar dataframe con domain_ids: {e}")
            return {"success": False, "message": str(e)}

        print("📆 Procesando eventos de siniestro...")
        try:
            for _, row in df_valid.iterrows():
                event_date = row["Fecha y hora de ocurrencia del siniestro"].strftime("%Y-%m-%d")
                domain_id = row["domain_id"]
                self.domain_service.process_domain_id_events(domain_id, event_date, event_date)
        except Exception as e:
            print(f"❌ Error al procesar eventos para los dominios: {e}")
            return {"success": False, "message": str(e)}

        print("✅ Pipeline completado.")
        return {"success": True, "message": "Pipeline ejecutado correctamente."}


