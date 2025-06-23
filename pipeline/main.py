# pipeline/main.py - Ejecutor del Portfolio Pipeline
import sys
import os
from datetime import datetime, timedelta

# Agregar la ruta padre para importar módulos hermanos
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

def main():
    """
    Punto de entrada principal para ejecutar el pipeline de portfolio desde /pipeline
    """
    print("🚀 Strix Portfolio Pipeline")
    print("=" * 50)
    print(f"📁 Ejecutando desde: {os.getcwd()}")
    
    try:
        # Verificar conexiones del sistema
        print("🔍 Verificando conexiones...")
        from security.services.health_check import health_check
        status = health_check()
        
        print(f"   PostgreSQL: {status.get('postgres', 'ERROR')}")
        print(f"   S3: {status.get('s3', 'ERROR')}")
        
        if not status.get("postgres") or not status.get("s3"):
            print("❌ Error en conexiones críticas. Abortando ejecución.")
            return False
        
        print("✅ Conexiones verificadas correctamente")
        
        # Intentar importar procesador paralelo, fallback a estándar
        try:
            from pipeline.services.portfolio_pipeline_parallel import ParallelPortfolioPipelineProcessor
            processor = ParallelPortfolioPipelineProcessor()
            processor_type = "PARALELO"
            print("🚀 Usando procesador PARALELO")
            
            # Mostrar configuración del sistema si está disponible
            try:
                import psutil
                cpu_count = psutil.cpu_count(logical=True)
                memory_gb = psutil.virtual_memory().total / (1024**3)
                print(f"   💻 CPUs detectadas: {cpu_count}")
                print(f"   🧠 RAM disponible: {memory_gb:.1f} GB")
                print(f"   🔧 Workers configurados: {processor.max_workers}")
            except ImportError:
                import multiprocessing
                print(f"   💻 CPUs detectadas: {multiprocessing.cpu_count()}")
                print(f"   🔧 Workers configurados: {processor.max_workers}")
                
        except ImportError as e:
            print("⚠️ Procesador paralelo no disponible, usando estándar...")
            print(f"   Razón: {e}")
            
            from pipeline.services.portfolio_pipeline import PortfolioPipelineProcessor
            processor = PortfolioPipelineProcessor()
            processor_type = "ESTÁNDAR"
            print("🔄 Usando procesador ESTÁNDAR")
        
        # Configurar fechas (personaliza estas fechas según necesites)
        start_date = datetime(2025, 4, 30).strftime("%Y-%m-%d")
        end_date = datetime(2025, 5, 1).strftime("%Y-%m-%d")
        
        print(f"📅 Rango de fechas: {start_date} hasta {end_date}")
        print(f"🔧 Tipo de procesador: {processor_type}")
        print("-" * 50)
        
        # Ejecutar pipeline
        print("🔄 Iniciando procesamiento...")
        start_time = datetime.now()
        
        if hasattr(processor, 'run_pipeline_parallel'):
            # Procesador paralelo con opciones avanzadas
            result = processor.run_pipeline_parallel(
                start_date=start_date,
                end_date=end_date,
                execution_mode="auto"  # auto, thread, process
            )
        else:
            # Procesador estándar - verificar si acepta parámetros
            import inspect
            sig = inspect.signature(processor.run_pipeline)
            
            if len(sig.parameters) >= 2:
                result = processor.run_pipeline(start_date, end_date)
            else:
                print("⚠️ Procesador estándar no acepta parámetros de fecha")
                result = processor.run_pipeline()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Mostrar resultados detallados
        print("=" * 50)
        print("📊 RESULTADO FINAL:")
        print(f"✅ Éxito: {result.get('success', False)}")
        print(f"📝 Mensaje: {result.get('message', 'Sin mensaje')}")
        print(f"⏱️ Duración total: {duration:.2f} segundos")
        
        # Métricas adicionales para procesador paralelo
        if result.get('workers_used'):
            print(f"🔧 Workers utilizados: {result['workers_used']}")
            
        if result.get('portfolios_processed'):
            successful = result.get('successful', 0)
            failed = result.get('failed', 0)
            total = result['portfolios_processed']
            success_rate = (successful / total * 100) if total > 0 else 0
            
            print(f"📂 Portfolios procesados: {total}")
            print(f"   ✅ Exitosos: {successful}")
            print(f"   ❌ Fallidos: {failed}")
            print(f"   📈 Tasa de éxito: {success_rate:.1f}%")
            
        if result.get('estimated_speedup'):
            speedup = result['estimated_speedup']
            print(f"🚀 Speedup estimado: {speedup:.2f}x")
            
            if speedup > 2:
                print("   🎉 ¡Excelente aceleración!")
            elif speedup > 1.5:
                print("   👍 Buena aceleración")
            elif speedup > 1.1:
                print("   👌 Aceleración moderada")
        
        # Estado final
        success = result.get('success', False)
        if success:
            print("\n🎉 Pipeline ejecutado exitosamente!")
        else:
            print("\n❌ Pipeline completado con errores")
            
        return success
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Soluciones posibles:")
        print("   - Instalar módulos en modo editable: pip install -e ../core -e ../security")
        print("   - Verificar que estés en el directorio correcto")
        print("   - Activar el entorno virtual: .\\venv\\Scripts\\Activate")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        print("\n🔍 Traceback completo:")
        traceback.print_exc()
        return False

def show_help():
    """
    Muestra información de ayuda
    """
    print("🚀 Strix Portfolio Pipeline")
    print("=" * 50)
    print("📋 DESCRIPCIÓN:")
    print("   Procesa eventos de portfolios desde S3 y los almacena en PostgreSQL")
    print()
    print("🔧 CONFIGURACIÓN:")
    print("   - Modifica las fechas en main() según necesites")
    print("   - El procesador paralelo se usa automáticamente si está disponible")
    print("   - Requiere conexión a PostgreSQL y S3")
    print()
    print("📁 ESTRUCTURA:")
    print("   pipeline/")
    print("   ├── main.py                    # Este archivo")
    print("   ├── services/")
    print("   │   ├── portfolio_pipeline.py          # Procesador estándar")
    print("   │   └── portfolio_pipeline_parallel.py # Procesador paralelo")
    print("   └── ...")
    print()
    print("🚀 EJECUCIÓN:")
    print("   python main.py                 # Ejecutar pipeline")
    print("   python main.py --help          # Mostrar esta ayuda")

if __name__ == "__main__":
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        show_help()
        sys.exit(0)
    
    print(f"🔹 Directorio actual: {os.getcwd()}")
    print(f"🐍 Python executable: {sys.executable}")
    print()
    
    success = main()
    
    if success:
        print("\n✅ Ejecución completada exitosamente!")
        sys.exit(0)
    else:
        print("\n❌ Ejecución falló. Revisar logs arriba.")
        sys.exit(1)