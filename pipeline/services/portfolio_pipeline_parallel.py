# pipeline/services/portfolio_pipeline_parallel.py
# Versión mejorada del PortfolioPipelineProcessor con soporte para paralelización

import concurrent.futures
import multiprocessing
import time
import psutil
from datetime import datetime, timedelta
from security.services.health_check import health_check
from core.services.portfolio_service import PortfolioService
from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork

class ParallelPortfolioPipelineProcessor:
    """
    Pipeline paralelo que:
    1. Chequea las conexiones de PostgreSQL y S3
    2. Obtiene todas las carteras activas
    3. Procesa los eventos en paralelo utilizando múltiples workers
    4. Proporciona métricas de rendimiento detalladas
    """

    def __init__(self, max_workers=None):
        self.portfolio_service = PortfolioService()
        self.max_workers = max_workers or self._calculate_optimal_workers()
    
    def _calculate_optimal_workers(self):
        """Calcula el número óptimo de workers basado en el sistema"""
        cpu_count = psutil.cpu_count(logical=True)
        memory_gb = psutil.virtual_memory().total / (1024**3)
        
        # Estrategia conservadora: dejar recursos para el sistema
        if memory_gb < 4:
            return min(2, cpu_count)
        elif memory_gb < 8:
            return min(4, cpu_count - 1)
        else:
            return min(8, cpu_count - 1)
    
    def _process_portfolio_batch(self, portfolio_batch, start_date, end_date, worker_id):
        """
        Procesa un lote de portfolios en un worker específico
        """
        results = []
        
        for portfolio_id in portfolio_batch:
            try:
                start_time = time.time()
                print(f"🔄 [Worker {worker_id}] Procesando Portfolio {portfolio_id}")
                
                # Procesar portfolio individual
                result = self.portfolio_service.process_portfolio_events(
                    portfolio_id, start_date, end_date
                )
                
                duration = time.time() - start_time
                
                results.append({
                    "portfolio_id": portfolio_id,
                    "success": result.get("success", True),
                    "duration": duration,
                    "worker_id": worker_id,
                    "processed_domains": result.get("processed_domains", [])
                })
                
                print(f"✅ [Worker {worker_id}] Portfolio {portfolio_id} completado ({duration:.2f}s)")
                
            except Exception as e:
                print(f"❌ [Worker {worker_id}] Error en Portfolio {portfolio_id}: {e}")
                results.append({
                    "portfolio_id": portfolio_id,
                    "success": False,
                    "error": str(e),
                    "worker_id": worker_id
                })
        
        return results
    
    def _distribute_portfolios(self, portfolios, num_workers):
        """Distribuye portfolios entre workers de manera equilibrada"""
        batches = [[] for _ in range(num_workers)]
        
        for i, portfolio in enumerate(portfolios):
            batch_index = i % num_workers
            batches[batch_index].append(portfolio)
        
        return [batch for batch in batches if batch]  # Filtrar lotes vacíos
    
    def run_pipeline_parallel(self, start_date=None, end_date=None, execution_mode="thread"):
        """
        Ejecuta el pipeline con procesamiento paralelo
        
        Args:
            start_date (str): Fecha inicio en formato YYYY-MM-DD
            end_date (str): Fecha fin en formato YYYY-MM-DD  
            execution_mode (str): "thread", "process", o "auto"
        
        Returns:
            dict: Resultados detallados del pipeline
        """
        start_time = time.time()
        
        # Configurar fechas por defecto
        if start_date is None:
            start_date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = datetime.utcnow().strftime("%Y-%m-%d")
        
        print(f"🚀 Iniciando pipeline paralelo ({execution_mode})")
        print(f"📅 Rango: {start_date} hasta {end_date}")
        print(f"🔧 Workers configurados: {self.max_workers}")
        
        try:
            # 1. Verificar conexiones
            print("🔍 Verificando conexiones...")
            status = health_check()
            if not status.get("postgres") or not status.get("s3"):
                return {
                    "success": False, 
                    "message": "Fallo en conexiones",
                    "connection_status": status
                }
            
            # 2. Obtener portfolios activos
            print("📥 Obteniendo carteras activas...")
            with SQLAlchemyUnitOfWork() as uow:
                active_portfolios = uow.portfolio_domains.get_active_portfolios()
            
            if not active_portfolios:
                return {
                    "success": False,
                    "message": "No hay carteras activas"
                }
            
            print(f"✅ {len(active_portfolios)} carteras encontradas")
            
            # 3. Distribuer portfolios entre workers
            portfolio_batches = self._distribute_portfolios(active_portfolios, self.max_workers)
            print(f"📊 Portfolios distribuidos en {len(portfolio_batches)} lotes")
            
            # 4. Ejecutar procesamiento paralelo
            all_results = []
            
            if execution_mode == "thread" or (execution_mode == "auto" and len(active_portfolios) <= 10):
                # ThreadPoolExecutor - mejor para I/O intensivo
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = {
                        executor.submit(
                            self._process_portfolio_batch, 
                            batch, start_date, end_date, i+1
                        ): i+1 for i, batch in enumerate(portfolio_batches)
                    }
                    
                    for future in concurrent.futures.as_completed(futures):
                        worker_id = futures[future]
                        try:
                            batch_results = future.result()
                            all_results.extend(batch_results)
                            
                            completed = len(all_results)
                            total = len(active_portfolios)
                            progress = (completed / total) * 100
                            print(f"📈 Progreso: {completed}/{total} ({progress:.1f}%)")
                            
                        except Exception as e:
                            print(f"❌ Worker {worker_id} falló: {e}")
            
            elif execution_mode == "process":
                # ProcessPoolExecutor - mejor para CPU intensivo
                with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = {
                        executor.submit(
                            self._process_portfolio_batch,
                            batch, start_date, end_date, i+1
                        ): i+1 for i, batch in enumerate(portfolio_batches)
                    }
                    
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            batch_results = future.result()
                            all_results.extend(batch_results)
                        except Exception as e:
                            print(f"❌ Error en proceso: {e}")
            
            # 5. Análisis de resultados
            end_time = time.time()
            total_duration = end_time - start_time
            
            successful = sum(1 for r in all_results if r.get("success", False))
            failed = len(all_results) - successful
            avg_duration = sum(r.get("duration", 0) for r in all_results) / len(all_results) if all_results else 0
            
            # Calcular speedup estimado
            sequential_time_estimate = avg_duration * len(all_results)
            speedup = sequential_time_estimate / total_duration if total_duration > 0 else 1
            
            result = {
                "success": successful > 0,
                "message": f"Pipeline paralelo completado: {successful}/{len(all_results)} exitosos",
                "execution_mode": execution_mode,
                "total_duration": total_duration,
                "portfolios_processed": len(all_results),
                "successful": successful,
                "failed": failed,
                "workers_used": len(portfolio_batches),
                "avg_duration_per_portfolio": avg_duration,
                "estimated_speedup": speedup,
                "start_date": start_date,
                "end_date": end_date,
                "results": all_results
            }
            
            # Log de resultados
            print("=" * 60)
            print("🎯 RESULTADO DEL PIPELINE PARALELO:")
            print(f"⏱️  Tiempo total: {total_duration:.2f} segundos")
            print(f"🔧 Workers utilizados: {len(portfolio_batches)}")
            print(f"✅ Portfolios exitosos: {successful}")
            print(f"❌ Portfolios fallidos: {failed}")
            print(f"📈 Duración promedio: {avg_duration:.2f}s por portfolio")
            print(f"🚀 Speedup estimado: {speedup:.2f}x")
            print("=" * 60)
            
            return result
            
        except Exception as e:
            print(f"❌ Error crítico en pipeline: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "success": False,
                "message": f"Error crítico: {e}",
                "total_duration": time.time() - start_time
            }
    
    def run_pipeline(self, start_date=None, end_date=None):
        """
        Método de compatibilidad con la interfaz original
        """
        return self.run_pipeline_parallel(start_date, end_date, "auto")

# Ejemplo de uso:
if __name__ == "__main__":
    processor = ParallelPortfolioPipelineProcessor(max_workers=4)
    result = processor.run_pipeline_parallel(
        start_date="2025-04-30",
        end_date="2025-05-01",
        execution_mode="thread"
    )
    print(f"Resultado final: {result['success']}")
