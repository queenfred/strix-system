# pipeline/main.py - CLI del Portfolio Pipeline
import sys
import os
import argparse
from datetime import datetime, timedelta

# Agregar la ruta padre para importar módulos hermanos
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

def create_parser():
    """
    Crea el parser de argumentos CLI
    """
    parser = argparse.ArgumentParser(
        prog='Strix Portfolio Pipeline',
        description='Procesador de eventos de portfolios desde S3 a PostgreSQL',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EJEMPLOS DE USO:
  python main.py                                    # Usar configuración por defecto
  python main.py --start 2025-04-30 --end 2025-05-01  # Fechas específicas
  python main.py --days 7                           # Procesar últimos 7 días
  python main.py --mode parallel --workers 6        # Modo paralelo con 6 workers
  python main.py --mode parallel --execution thread # Forzar ThreadPoolExecutor
  python main.py --verbose --dry-run                # Simulación con detalles
  python main.py --portfolio-ids 1,2,3              # Procesar portfolios específicos
  python main.py --skip-health-check --quiet        # Ejecución rápida y silenciosa
  python main.py --today                            # Solo procesar eventos de hoy

CONFIGURACIÓN:
  Las conexiones a PostgreSQL y S3 se configuran mediante variables de entorno
  en el archivo .env en la raíz del proyecto.

MODOS DE PROCESAMIENTO:
  auto     - Detecta automáticamente el mejor procesador disponible
  parallel - Fuerza el uso del procesador paralelo (requiere instalación)
  standard - Usa el procesador estándar (single-threaded)

MODOS DE EJECUCIÓN PARALELA:
  auto     - Detecta automáticamente (thread para I/O, process para CPU)
  thread   - ThreadPoolExecutor (recomendado para operaciones I/O como S3/DB)
  process  - ProcessPoolExecutor (para operaciones CPU intensivas)
        """
    )
    
    # === GRUPO DE FECHAS ===
    date_group = parser.add_argument_group('Configuración de fechas')
    
    date_group.add_argument(
        '--start', '--start-date',
        type=str,
        metavar='YYYY-MM-DD',
        help='Fecha de inicio en formato YYYY-MM-DD (default: ayer)'
    )
    
    date_group.add_argument(
        '--end', '--end-date',
        type=str, 
        metavar='YYYY-MM-DD',
        help='Fecha de fin en formato YYYY-MM-DD (default: hoy)'
    )
    
    date_group.add_argument(
        '--days',
        type=int,
        metavar='N',
        help='Procesar últimos N días (alternativa a --start/--end)'
    )
    
    date_group.add_argument(
        '--today',
        action='store_true',
        help='Procesar solo eventos de hoy'
    )
    
    date_group.add_argument(
        '--yesterday', 
        action='store_true',
        help='Procesar solo eventos de ayer'
    )
    
    # === GRUPO DE PROCESAMIENTO ===
    processing_group = parser.add_argument_group('Configuración de procesamiento')
    
    processing_group.add_argument(
        '--mode',
        choices=['auto', 'parallel', 'standard'],
        default='auto',
        help='Modo de procesamiento (default: auto)'
    )
    
    processing_group.add_argument(
        '--workers',
        type=int,
        metavar='N',
        help='Número de workers paralelos (default: auto-detectar)'
    )
    
    processing_group.add_argument(
        '--execution-mode',
        choices=['auto', 'thread', 'process'],
        default='auto',
        dest='execution_mode',
        help='Modo de ejecución paralela (default: auto)'
    )
    
    processing_group.add_argument(
        '--portfolio-ids',
        type=str,
        metavar='ID1,ID2,ID3',
        help='Procesar solo portfolios específicos (separados por comas)'
    )
    
    # === GRUPO DE CONFIGURACIÓN ===
    config_group = parser.add_argument_group('Configuración de ejecución')
    
    config_group.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar información detallada durante la ejecución'
    )
    
    config_group.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Mostrar solo información esencial (opuesto a --verbose)'
    )
    
    config_group.add_argument(
        '--dry-run',
        action='store_true',
        help='Simular ejecución sin procesar datos reales'
    )
    
    config_group.add_argument(
        '--skip-health-check',
        action='store_true',
        help='Saltar verificación de conexiones PostgreSQL/S3'
    )
    
    config_group.add_argument(
        '--force',
        action='store_true',
        help='Continuar ejecución aunque falle la verificación de salud'
    )
    
    # === GRUPO DE INFORMACIÓN ===
    info_group = parser.add_argument_group('Información del sistema')
    
    info_group.add_argument(
        '--show-config',
        action='store_true',
        help='Mostrar configuración del sistema y salir'
    )
    
    info_group.add_argument(
        '--list-portfolios', 
        action='store_true',
        help='Listar portfolios activos y salir'
    )
    
    info_group.add_argument(
        '--version',
        action='version',
        version='Strix Portfolio Pipeline v1.0.0'
    )
    
    return parser

def validate_args(args):
    """
    Valida los argumentos de entrada
    """
    errors = []
    
    # Validar que verbose y quiet no se usen juntos
    if args.verbose and args.quiet:
        errors.append("--verbose y --quiet no pueden usarse simultáneamente")
    
    # Validar fechas si se proporcionan
    if args.start:
        try:
            datetime.strptime(args.start, '%Y-%m-%d')
        except ValueError:
            errors.append(f"Formato de fecha inválido para --start: {args.start} (usar YYYY-MM-DD)")
    
    if args.end:
        try:
            datetime.strptime(args.end, '%Y-%m-%d')
        except ValueError:
            errors.append(f"Formato de fecha inválido para --end: {args.end} (usar YYYY-MM-DD)")
    
    # Validar que no se usen múltiples opciones de fecha
    date_options = sum([
        bool(args.start or args.end),
        bool(args.days),
        args.today,
        args.yesterday
    ])
    
    if date_options > 1:
        errors.append("Solo puede usarse una opción de fecha: --start/--end, --days, --today, o --yesterday")
    
    # Validar workers
    if args.workers and args.workers < 1:
        errors.append("--workers debe ser un número positivo")
    
    # Validar portfolio-ids
    if args.portfolio_ids:
        try:
            portfolio_ids = [int(id.strip()) for id in args.portfolio_ids.split(',')]
            if not all(id > 0 for id in portfolio_ids):
                errors.append("Todos los portfolio IDs deben ser números positivos")
        except ValueError:
            errors.append("portfolio-ids debe ser una lista de números separados por comas")
    
    return errors

def calculate_dates(args):
    """
    Calcula las fechas de inicio y fin basado en los argumentos
    """
    now = datetime.now()
    
    if args.today:
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif args.yesterday:
        yesterday = now - timedelta(days=1)
        start_date = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif args.days:
        end_date = now
        start_date = now - timedelta(days=args.days)
    else:
        # Usar fechas específicas o por defecto
        if args.end:
            end_date = datetime.strptime(args.end, '%Y-%m-%d')
        else:
            end_date = now
        
        if args.start:
            start_date = datetime.strptime(args.start, '%Y-%m-%d')
        else:
            start_date = end_date - timedelta(days=1)
    
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

def check_system_health(args):
    """
    Verifica el estado de las conexiones del sistema
    """
    if args.skip_health_check:
        if not args.quiet:
            print("⚠️ Saltando verificación de conexiones...")
        return True
    
    try:
        if not args.quiet:
            print("🔍 Verificando conexiones del sistema...")
        
        from security.services.health_check import health_check
        status = health_check()
        
        postgres_ok = status.get('postgres') == 'OK'
        s3_ok = status.get('s3') == 'OK'
        
        if not args.quiet:
            print(f"   PostgreSQL: {'✅' if postgres_ok else '❌'} {status.get('postgres', 'ERROR')}")
            print(f"   S3: {'✅' if s3_ok else '❌'} {status.get('s3', 'ERROR')}")
        
        if not postgres_ok or not s3_ok:
            if args.force:
                if not args.quiet:
                    print("⚠️ Continuando con --force a pesar de errores de conexión...")
                return True
            else:
                print("❌ Error en conexiones críticas")
                print("💡 Usa --force para continuar o --skip-health-check para saltar verificación")
                return False
        
        if not args.quiet:
            print("✅ Todas las conexiones verificadas")
        return True
        
    except Exception as e:
        if args.force:
            if not args.quiet:
                print(f"⚠️ Error en verificación: {e}, continuando con --force...")
            return True
        else:
            print(f"❌ Error en verificación de salud: {e}")
            return False

def show_system_config(args):
    """
    Muestra la configuración del sistema
    """
    print("🔧 CONFIGURACIÓN DEL SISTEMA")
    print("=" * 50)
    
    # Información básica
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"🐍 Python executable: {sys.executable}")
    print(f"📦 Directorio del script: {current_dir}")
    
    # Información de CPU y memoria
    try:
        import psutil
        print(f"💻 CPUs disponibles: {psutil.cpu_count(logical=True)}")
        print(f"🧠 Memoria RAM: {psutil.virtual_memory().total / (1024**3):.1f} GB")
        print(f"⚡ Uso actual CPU: {psutil.cpu_percent(interval=1)}%")
    except ImportError:
        import multiprocessing
        print(f"💻 CPUs disponibles: {multiprocessing.cpu_count()}")
        print("🧠 Memoria RAM: No disponible (psutil no instalado)")
    
    # Verificar procesadores disponibles
    print("\n🚀 PROCESADORES DISPONIBLES:")
    
    try:
        from pipeline.services.portfolio_pipeline_parallel import ParallelPortfolioPipelineProcessor
        processor = ParallelPortfolioPipelineProcessor()
        print(f"   ✅ Procesador paralelo (workers: {processor.max_workers})")
    except ImportError as e:
        print(f"   ❌ Procesador paralelo: {e}")
    
    try:
        from pipeline.services.portfolio_pipeline import PortfolioPipelineProcessor
        print("   ✅ Procesador estándar")
    except ImportError as e:
        print(f"   ❌ Procesador estándar: {e}")
    
    # Verificar conexiones
    print("\n🔗 ESTADO DE CONEXIONES:")
    try:
        from security.services.health_check import health_check
        status = health_check()
        for service, state in status.items():
            icon = "✅" if state == "OK" else "❌"
            print(f"   {icon} {service.upper()}: {state}")
    except Exception as e:
        print(f"   ❌ Error verificando conexiones: {e}")

def list_portfolios(args):
    """
    Lista los portfolios activos
    """
    print("📁 PORTFOLIOS ACTIVOS")
    print("=" * 50)
    
    try:
        from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
        
        with SQLAlchemyUnitOfWork() as uow:
            active_portfolios = uow.portfolio_domains.get_active_portfolios()
            all_portfolios = uow.portfolios.get_all_portfolios()
        
        print(f"📊 Total portfolios en sistema: {len(all_portfolios)}")
        print(f"🔄 Portfolios activos: {len(active_portfolios)}")
        
        if not args.quiet:
            print("\n📋 LISTA DE PORTFOLIOS:")
            for portfolio in all_portfolios:
                status = "🟢 ACTIVO" if portfolio['id'] in active_portfolios else "🔴 INACTIVO"
                print(f"   ID: {portfolio['id']:2d} | {status} | {portfolio['name']}")
        
        if active_portfolios:
            print(f"\n💡 Para procesar portfolios específicos: --portfolio-ids {','.join(map(str, active_portfolios[:3]))}")
        
    except Exception as e:
        print(f"❌ Error obteniendo portfolios: {e}")

def create_processor(args):
    """
    Crea el procesador apropiado basado en los argumentos
    """
    if args.mode == 'auto':
        # Auto-detectar mejor procesador
        try:
            from pipeline.services.portfolio_pipeline_parallel import ParallelPortfolioPipelineProcessor
            processor = ParallelPortfolioPipelineProcessor(max_workers=args.workers)
            processor_type = "PARALELO (auto-detectado)"
            return processor, processor_type
        except ImportError:
            pass
    
    if args.mode in ['auto', 'parallel']:
        try:
            from pipeline.services.portfolio_pipeline_parallel import ParallelPortfolioPipelineProcessor
            processor = ParallelPortfolioPipelineProcessor(max_workers=args.workers)
            processor_type = "PARALELO"
            return processor, processor_type
        except ImportError:
            if args.mode == 'parallel':
                raise ImportError("❌ Procesador paralelo no disponible. Instalar: pip install psutil")
    
    # Fallback a procesador estándar
    from pipeline.services.portfolio_pipeline import PortfolioPipelineProcessor
    processor = PortfolioPipelineProcessor()
    processor_type = "ESTÁNDAR"
    return processor, processor_type

def run_pipeline(processor, processor_type, start_date, end_date, args):
    """
    Ejecuta el pipeline con la configuración especificada
    """
    if args.dry_run:
        print("🧪 MODO DRY-RUN: Simulando ejecución...")
        print(f"   📊 Procesador: {processor_type}")
        print(f"   📅 Fechas: {start_date} a {end_date}")
        
        if hasattr(processor, 'max_workers'):
            print(f"   🔧 Workers: {processor.max_workers}")
        
        if args.portfolio_ids:
            portfolio_list = [int(id.strip()) for id in args.portfolio_ids.split(',')]
            print(f"   📁 Portfolios específicos: {portfolio_list}")
        
        print("✅ Dry-run completado exitosamente")
        return {"success": True, "message": "Dry-run exitoso", "dry_run": True}
    
    if not args.quiet:
        print(f"🚀 Ejecutando pipeline {processor_type}")
        print(f"📅 Rango: {start_date} hasta {end_date}")
        
        if args.verbose and hasattr(processor, 'max_workers'):
            print(f"🔧 Workers configurados: {processor.max_workers}")
    
    start_time = datetime.now()
    
    try:
        if hasattr(processor, 'run_pipeline_parallel'):
            # Procesador paralelo
            result = processor.run_pipeline_parallel(
                start_date=start_date,
                end_date=end_date,
                execution_mode=args.execution_mode
            )
        else:
            # Procesador estándar
            import inspect
            sig = inspect.signature(processor.run_pipeline)
            
            if len(sig.parameters) >= 2:
                result = processor.run_pipeline(start_date, end_date)
            else:
                if not args.quiet:
                    print("⚠️ Procesador estándar no acepta parámetros de fecha")
                result = processor.run_pipeline()
        
        duration = (datetime.now() - start_time).total_seconds()
        result['execution_duration'] = duration
        
        return result
        
    except Exception as e:
        print(f"❌ Error durante ejecución: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return {"success": False, "message": f"Error: {e}"}

def print_results(result, args):
    """
    Muestra los resultados del pipeline
    """
    if args.quiet and result.get('success'):
        # Modo quiet solo muestra resultado final si es exitoso
        return result.get('success', False)
    
    print("=" * 60)
    print("📊 RESULTADO FINAL:")
    
    success = result.get('success', False)
    print(f"✅ Éxito: {'SÍ' if success else 'NO'}")
    
    if not args.quiet or not success:
        print(f"📝 Mensaje: {result.get('message', 'Sin mensaje')}")
    
    if result.get('execution_duration') and not args.quiet:
        duration = result['execution_duration']
        print(f"⏱️ Duración: {duration:.2f} segundos")
    
    if (args.verbose or not success) and not result.get('dry_run'):
        print("\n📈 MÉTRICAS DETALLADAS:")
        
        if result.get('workers_used'):
            print(f"   🔧 Workers utilizados: {result['workers_used']}")
        
        if result.get('portfolios_processed'):
            total = result['portfolios_processed']
            successful = result.get('successful', 0)
            failed = result.get('failed', 0)
            success_rate = (successful / total * 100) if total > 0 else 0
            
            print(f"   📂 Portfolios procesados: {total}")
            print(f"   ✅ Exitosos: {successful}")
            print(f"   ❌ Fallidos: {failed}")
            print(f"   📈 Tasa de éxito: {success_rate:.1f}%")
        
        if result.get('estimated_speedup'):
            speedup = result['estimated_speedup']
            print(f"   🚀 Speedup: {speedup:.2f}x")
        
        if result.get('avg_duration_per_portfolio'):
            avg_time = result['avg_duration_per_portfolio']
            print(f"   📊 Tiempo promedio por portfolio: {avg_time:.2f}s")
    
    return success

def main():
    """
    Función principal del CLI
    """
    parser = create_parser()
    args = parser.parse_args()
    
    # Validar argumentos
    errors = validate_args(args)
    if errors:
        print("❌ ERRORES EN ARGUMENTOS:")
        for error in errors:
            print(f"   • {error}")
        print(f"\nUsa 'python {os.path.basename(__file__)} --help' para ver la ayuda completa")
        return False
    
    # Comandos de información (no ejecutan pipeline)
    if args.show_config:
        show_system_config(args)
        return True
    
    if args.list_portfolios:
        list_portfolios(args)
        return True
    
    # Header de ejecución
    if not args.quiet:
        print("🚀 Strix Portfolio Pipeline")
        print("=" * 50)
        
        if args.verbose:
            print(f"📁 Directorio: {os.getcwd()}")
            print(f"🔧 Argumentos: {vars(args)}")
            print()
    
    try:
        # Verificar sistema
        if not check_system_health(args):
            return False
        
        # Calcular fechas
        start_date, end_date = calculate_dates(args)
        
        # Crear procesador
        processor, processor_type = create_processor(args)
        
        if not args.quiet:
            print(f"✅ Procesador: {processor_type}")
        
        # Ejecutar pipeline
        result = run_pipeline(processor, processor_type, start_date, end_date, args)
        
        # Mostrar resultados
        success = print_results(result, args)
        
        return success
        
    except KeyboardInterrupt:
        print("\n⚠️ Ejecución interrumpida por el usuario")
        return False
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)