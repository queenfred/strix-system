from security.services.health_check import health_check
from core.services.portfolio_service import PortfolioService
from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from datetime import datetime, timedelta

class PortfolioPipelineProcessor:
    """
    Pipeline que:
    1. Chequea las conexiones de PostgreSQL y S3.
    2. Obtiene todas las carteras activas (portfolios con dominios activos).
    3. Procesa los eventos del día anterior hasta el día actual.
    """

    def __init__(self):
        self.portfolio_service = PortfolioService()

    def run_pipeline(self):
        """
        Ejecuta todo el pipeline de procesamiento de eventos.
        """
        print("🔍 Verificando conexiones...")
        status = health_check()
        if not status.get("postgres") or not status.get("s3"):
            print("❌ Error en las conexiones. Abortando proceso.")
            return {"success": False, "message": "Fallo en conexión a PostgreSQL o S3."}
        print("✅ Conexiones correctas.")

        print("📥 Obteniendo carteras activas...")
        try:
            with SQLAlchemyUnitOfWork() as uow:
                active_portfolios = uow.portfolio_domains.get_active_portfolios()
        except Exception as e:
            print(f"❌ Error al obtener carteras activas: {e}")
            return {"success": False, "message": str(e)}

        if not active_portfolios:
            print("⚠ No hay carteras activas para procesar.")
            return {"success": False, "message": "No hay carteras activas."}
        print(f"✅ {len(active_portfolios)} carteras activas encontradas.")

        # Calcular el rango de fechas (día anterior hasta hoy)
        #start_date = (datetime.utcnow() - timedelta(days=10)).strftime("%Y-%m-%d")
        #end_date = datetime.utcnow().strftime("%Y-%m-%d")
        start_date = datetime(2025, 4, 1).strftime("%Y-%m-%d")
        end_date = datetime(2025, 4, 30).strftime("%Y-%m-%d")
        print(f"📆 Procesando eventos desde {start_date} hasta {end_date}...")
        for portfolio_id in active_portfolios:
            result = self.portfolio_service.process_portfolio_events(portfolio_id, start_date, end_date)
            print(f"📊 Resultados para Portfolio {portfolio_id}: {result}")

        print("✅ Pipeline completado.")
        return {"success": True, "message": "Pipeline ejecutado correctamente."}
