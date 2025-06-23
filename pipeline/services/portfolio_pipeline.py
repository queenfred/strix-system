# Modificación sugerida para pipeline/services/portfolio_pipeline.py

from security.services.health_check import health_check
from core.services.portfolio_service import PortfolioService
from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from datetime import datetime, timedelta

class PortfolioPipelineProcessor:
    """
    Pipeline que:
    1. Chequea las conexiones de PostgreSQL y S3.
    2. Obtiene todas las carteras activas (portfolios con dominios activos).
    3. Procesa los eventos en el rango de fechas especificado.
    """

    def __init__(self):
        self.portfolio_service = PortfolioService()

    def run_pipeline(self, start_date=None, end_date=None):
        """
        Ejecuta todo el pipeline de procesamiento de eventos.
        
        Args:
            start_date (str, optional): Fecha de inicio en formato "YYYY-MM-DD". 
                                       Si no se proporciona, usa 10 días atrás.
            end_date (str, optional): Fecha de fin en formato "YYYY-MM-DD".
                                     Si no se proporciona, usa fecha actual.
        
        Returns:
            dict: Resultado del pipeline con 'success' y 'message'
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

        # Configurar rango de fechas
        if start_date is None:
            start_date = (datetime.utcnow() - timedelta(days=10)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = datetime.utcnow().strftime("%Y-%m-%d")
            
        print(f"📆 Procesando eventos desde {start_date} hasta {end_date}...")
        
        # Procesar cada portfolio
        for portfolio_id in active_portfolios:
            result = self.portfolio_service.process_portfolio_events(portfolio_id, start_date, end_date)
            print(f"📊 Resultados para Portfolio {portfolio_id}: {result}")

        print("✅ Pipeline completado.")
        return {"success": True, "message": "Pipeline ejecutado correctamente."}