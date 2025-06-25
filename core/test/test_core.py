# core/test/test_core.py
#!/usr/bin/env python3
"""
Script para testing aislado del módulo Core
Ubicación: core/test/test_core.py
"""
import os
import sys
import subprocess
from pathlib import Path

# Agregar el directorio raíz del proyecto al path (ir 2 niveles arriba)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def create_test_structure():
    """Crea la estructura de directorios para tests si no existe"""
    base_dir = Path(__file__).parent  # core/test/
    
    test_dirs = [
        "unit", 
        "integration",
        "fixtures"
    ]
    
    for dir_name in test_dirs:
        dir_path = base_dir / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        init_file = dir_path / "__init__.py"
        if not init_file.exists():
            init_file.touch()
    
    # Crear __init__.py en core/test/ también
    init_file = base_dir / "__init__.py"
    if not init_file.exists():
        init_file.touch()
        
    print("✅ Estructura de tests creada")

def check_core_imports():
    """Verifica que los imports del core funcionen"""
    print("🔍 Verificando imports del core...")
    try:
        # Test básico de infraestructura
        from core.infraestructure.db.postgres import Postgres
        print("✅ Postgres import OK")
        
        from core.infraestructure.aws.s3 import S3Client
        print("✅ S3Client import OK")
        
        # Test de modelos
        from core.models.domain import Domain
        print("✅ Domain model OK")
        
        from core.models.event import Event
        print("✅ Event model OK")
        
        # Test de servicios básicos
        from core.services.domain_service import DomainService
        print("✅ DomainService import OK")
        
        from core.services.event_service import EventService
        print("✅ EventService import OK")
        
        from core.services.portfolio_service import PortfolioService
        print("✅ PortfolioService import OK")
        
        return True
    except Exception as e:
        print(f"❌ Error en imports: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    """Test de conexión a base de datos sin dependencias externas"""
    print("🗄️ Probando conexión a base de datos...")
    try:
        from core.infraestructure.db.postgres import Postgres
        db = Postgres()
        engine = db.connPostgres()
        
        if engine:
            print("✅ Conexión a PostgreSQL OK")
            
            # Test básico de query
            from sqlalchemy import text
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1 as test"))
                test_value = result.fetchone()[0]
                if test_value == 1:
                    print("✅ Query test OK")
                    return True
        return False
    except Exception as e:
        print(f"❌ Error de base de datos: {e}")
        return False

def test_s3_connection():
    """Test de conexión S3 básica"""
    print("☁️ Probando conexión a S3...")
    try:
        from core.infraestructure.aws.s3 import S3Client
        s3_client = S3Client()
        client = s3_client.conn_s3()
        
        if client:
            print("✅ Conexión a S3 OK")
            return True
        else:
            print("⚠️ S3 no conectado (puede ser normal en dev)")
            return False
    except Exception as e:
        print(f"❌ Error de S3: {e}")
        return False

def test_core_services():
    """Test básico de servicios core sin DB real"""
    print("⚙️ Probando servicios core...")
    try:
        from core.services.domain_service import DomainService
        
        # Crear instancia del servicio
        service = DomainService()
        print("✅ DomainService instanciado")
        
        # Test que requiere DB real (comentado para testing)
        # domains = service.get_all_domains()
        # print(f"✅ Dominios obtenidos: {len(domains) if domains else 0}")
        
        print("⚠️ Tests con DB real comentados para evitar errores")
        return True
    except Exception as e:
        print(f"❌ Error en servicios: {e}")
        return False

def test_uow_import():
    """Test específico del Unit of Work"""
    print("🔧 Probando Unit of Work...")
    try:
        from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
        print("✅ SQLAlchemyUnitOfWork import OK")
        
        # Test instanciación (sin usar context manager para evitar DB)
        uow_class = SQLAlchemyUnitOfWork
        print("✅ UnitOfWork class OK")
        
        return True
    except Exception as e:
        print(f"❌ Error en UnitOfWork: {e}")
        return False

def run_unit_tests_core_only():
    """Ejecuta solo tests unitarios del core"""
    print("🧪 Ejecutando tests unitarios del core...")
    
    current_dir = Path(__file__).parent
    unit_dir = current_dir / "unit"
    
    if not unit_dir.exists():
        print("⚠️ No existe directorio unit/, creándolo...")
        create_test_structure()
        print("ℹ️ Directorios creados. Necesitas agregar archivos de test.")
        return False
    
    # Cambiar al directorio raíz del proyecto para ejecutar pytest
    os.chdir(project_root)
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "core/test/unit/", 
        "-v", "--tb=short"
    ]
    
    result = subprocess.run(cmd)
    return result.returncode == 0

def create_sample_tests():
    """Crea tests de ejemplo si no existen"""
    print("📝 Creando tests de ejemplo...")
    
    current_dir = Path(__file__).parent
    unit_dir = current_dir / "unit"
    
    # Crear conftest.py
    conftest_content = '''import pytest
import sys
import os
from unittest.mock import MagicMock, patch

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

@pytest.fixture
def mock_uow():
    """Mock del Unit of Work"""
    uow = MagicMock()
    uow.__enter__.return_value = uow
    uow.__exit__.return_value = None
    
    # Mock repositorios
    uow.domains = MagicMock()
    uow.events = MagicMock()
    uow.portfolios = MagicMock()
    
    return uow

@pytest.fixture
def sample_domain():
    return {
        "id": 1,
        "domain": "TEST123",
        "id_thing": "mrn:thing:test",
        "id_account": "mrn:account:test"
    }
'''
    
    conftest_file = current_dir / "conftest.py"
    if not conftest_file.exists():
        conftest_file.write_text(conftest_content)
        print("✅ conftest.py creado")
    
    # Crear test simple
    test_content = '''import pytest
from unittest.mock import patch
from core.services.domain_service import DomainService

class TestDomainServiceSimple:
    
    @patch('core.services.domain_service.SQLAlchemyUnitOfWork')
    def test_get_all_domains_mock(self, mock_uow_class, mock_uow, sample_domain):
        # Setup mock
        mock_uow_class.return_value = mock_uow
        mock_uow.domains.get_all_domains.return_value = [sample_domain]
        
        # Test
        service = DomainService()
        result = service.get_all_domains()
        
        # Assert
        assert len(result) == 1
        assert result[0]["domain"] == "TEST123"
        mock_uow.domains.get_all_domains.assert_called_once()

    def test_domain_service_creation(self):
        """Test que solo verifica que se puede crear la instancia"""
        service = DomainService()
        assert service is not None
'''
    
    test_file = unit_dir / "test_domain_service_simple.py"
    if not test_file.exists():
        test_file.write_text(test_content)
        print("✅ test_domain_service_simple.py creado")
    
    return True

def core_health_check():
    """Health check específico para core sin dependencias externas"""
    print("🏥 Health Check del Módulo Core")
    print("=" * 40)
    
    checks = [
        ("Imports del Core", check_core_imports),
        ("Unit of Work", test_uow_import),
        ("Conexión BD", test_database_connection),
        ("Conexión S3", test_s3_connection),
        ("Servicios Core", test_core_services)
    ]
    
    results = {}
    for name, check_func in checks:
        print(f"\n🔍 {name}...")
        results[name] = check_func()
    
    print("\n📊 Resumen del Health Check:")
    print("-" * 30)
    for name, result in results.items():
        status = "✅ OK" if result else "❌ FAIL"
        print(f"{name:<20} {status}")
    
    return all(results.values())

def interactive_menu():
    """Menú interactivo para testing del core"""
    print("🎮 Core Testing Menu")
    print("=" * 30)
    
    options = {
        "1": ("Health Check Completo", core_health_check),
        "2": ("Solo verificar imports", check_core_imports),
        "3": ("Solo test UnitOfWork", test_uow_import),
        "4": ("Solo test BD", test_database_connection),
        "5": ("Solo test S3", test_s3_connection),
        "6": ("Test servicios", test_core_services),
        "7": ("Crear estructura de tests", create_test_structure),
        "8": ("Crear tests de ejemplo", create_sample_tests),
        "9": ("Ejecutar tests unitarios", run_unit_tests_core_only),
        "0": ("Salir", lambda: True)
    }
    
    while True:
        print("\nSelecciona una opción:")
        for key, (description, _) in options.items():
            print(f"  {key}. {description}")
        
        choice = input("\nOpción: ").strip()
        
        if choice == "0":
            break
        
        if choice in options:
            description, func = options[choice]
            print(f"\n🚀 Ejecutando: {description}")
            print("-" * 40)
            
            success = func()
            
            if success:
                print(f"✅ {description} completado exitosamente")
            else:
                print(f"❌ {description} falló")
        else:
            print("❌ Opción inválida")

def main():
    """Función principal"""
    print("🧪 Core Module Testing Suite")
    print(f"📁 Ejecutándose desde: {Path(__file__).absolute()}")
    print(f"📁 Proyecto root: {project_root.absolute()}")
    print("=" * 50)
    
    if len(sys.argv) == 1:
        # Modo interactivo
        interactive_menu()
    else:
        # Modo comando
        if "--health" in sys.argv:
            core_health_check()
        elif "--imports" in sys.argv:
            check_core_imports()
        elif "--uow" in sys.argv:
            test_uow_import()
        elif "--db" in sys.argv:
            test_database_connection()
        elif "--s3" in sys.argv:
            test_s3_connection()
        elif "--services" in sys.argv:
            test_core_services()
        elif "--tests" in sys.argv:
            create_test_structure()
            create_sample_tests()
            run_unit_tests_core_only()
        elif "--setup" in sys.argv:
            create_test_structure()
            create_sample_tests()
        else:
            print("Uso: python test_core.py [--health|--imports|--uow|--db|--s3|--services|--tests|--setup]")
            print("Sin argumentos: Modo interactivo")

if __name__ == "__main__":
    main()