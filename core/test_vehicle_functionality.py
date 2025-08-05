# test_vehicle_features.py
"""
Script para probar todas las funcionalidades nuevas de vehículos en el sistema.
Ejecuta pruebas de creación, actualización, filtrado y sincronización de domains con info de vehículos.
"""

from core.services.domain_service import DomainService
from core.services.vehicle_service import VehicleService
from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from datetime import datetime
import json

def print_separator(title):
    """Imprime un separador visual con título"""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def print_result(operation, result):
    """Imprime el resultado de una operación de forma legible"""
    print(f"\n📋 {operation}:")
    if isinstance(result, dict):
        print(json.dumps(result, indent=2, default=str))
    elif isinstance(result, list):
        print(f"📊 Total de elementos: {len(result)}")
        for i, item in enumerate(result[:3]):  # Mostrar solo los primeros 3
            print(f"   [{i+1}] {item}")
        if len(result) > 3:
            print(f"   ... y {len(result) - 3} elementos más")
    else:
        print(f"   {result}")

def test_domain_creation_with_vehicle_info():
    """Prueba la creación de domains con información de vehículos"""
    print_separator("PRUEBA 1: Creación de Domains con Información de Vehículos")
    
    domain_service = DomainService()
    
    # Datos de prueba para crear domains con info de vehículos
    test_domains = [
        {
            "domain_name": "TEST001",
            "id_thing": "mrn:thing:vehicle:test001",
            "id_account": "mrn:account:test001",
            "subtype": "Sedán",
            "color": "Rojo",
            "make": "Toyota",
            "model": "Corolla",
            "year": 2022,
            "gps": "GPS-2022-A"
        },
        {
            "domain_name": "TEST002",
            "id_thing": "mrn:thing:vehicle:test002", 
            "id_account": "mrn:account:test002",
            "subtype": "SUV",
            "color": "Azul",
            "make": "Honda",
            "model": "CR-V",
            "year": 2023,
            "gps": "GPS-2023-B"
        },
        {
            "domain_name": "TEST003",
            "id_thing": "mrn:thing:vehicle:test003",
            "id_account": "mrn:account:test003", 
            "subtype": "Hatchback",
            "color": "Blanco",
            "make": "Ford",
            "model": "Fiesta",
            "year": 2021,
            "gps": "GPS-2021-C"
        }
    ]
    
    created_domains = []
    
    for domain_data in test_domains:
        result = domain_service.create_domain_with_current_datetime(**domain_data)
        created_domains.append(result)
        print_result(f"Domain creado: {domain_data['domain_name']}", result)
    
    return created_domains

def test_domain_filtering():
    """Prueba el filtrado de domains por características de vehículos"""
    print_separator("PRUEBA 2: Filtrado de Domains por Características")
    
    domain_service = DomainService()
    
    # Filtrar por marca Toyota
    toyotas = domain_service.get_domains_by_vehicle_criteria(make="Toyota")
    print_result("Domains con marca Toyota", toyotas)
    
    # Filtrar por color Azul
    azules = domain_service.get_domains_by_vehicle_criteria(color="Azul")
    print_result("Domains de color Azul", azules)
    
    # Filtrar por año 2023
    año_2023 = domain_service.get_domains_by_vehicle_criteria(year=2023)
    print_result("Domains del año 2023", año_2023)
    
    # Filtro combinado: SUVs Rojos
    suvs_rojos = domain_service.get_domains_by_vehicle_criteria(
        # subtype="SUV",  # Nota: subtype no está implementado en el filtro actual
        color="Rojo"
    )
    print_result("Domains SUVs de color Rojo", suvs_rojos)
    
    return {"toyotas": len(toyotas), "azules": len(azules), "año_2023": len(año_2023)}

def test_domain_updates():
    """Prueba la actualización de información de vehículos en domains existentes"""
    print_separator("PRUEBA 3: Actualización de Información de Vehículos")
    
    domain_service = DomainService()
    
    # Obtener un domain para actualizar (usaremos uno de los creados)
    all_domains = domain_service.get_all_domains()
    
    if all_domains:
        domain_to_update = all_domains[0]
        domain_id = domain_to_update["id"]
        
        print_result("Domain antes de actualizar", domain_to_update)
        
        # Actualizar información del vehículo
        updated_info = {
            "color": "Verde Metalizado",
            "make": "Toyota",
            "model": "Prius Híbrido",
            "year": 2024,
            "gps": "GPS-2024-Premium"
        }
        
        result = domain_service.update_domain_vehicle_info(domain_id, **updated_info)
        print_result("Domain después de actualizar", result)
        
        return result
    else:
        print("⚠️ No hay domains disponibles para actualizar")
        return None

def test_vehicle_service_integration():
    """Prueba la integración con VehicleService"""
    print_separator("PRUEBA 4: Integración con VehicleService")
    
    with SQLAlchemyUnitOfWork() as uow:
        vehicle_service = VehicleService(uow)
        
        # Intentar crear domains desde la tabla de vehículos (con límite pequeño)
        result = vehicle_service.create_domains_from_vehicles(limit=5)
        print_result("Creación desde strix.vvehicle", result)
        
        # Intentar sincronización de fechas
        sync_result = vehicle_service.sync_domains_with_vehicle_dates()
        print_result("Sincronización de fechas", sync_result)
        
        return result

def test_domain_statistics():
    """Prueba la obtención de estadísticas de domains"""
    print_separator("PRUEBA 5: Estadísticas de Domains")
    
    domain_service = DomainService()
    
    # Obtener estadísticas generales
    stats = domain_service.get_domain_statistics()
    print_result("Estadísticas generales", stats)
    
    # Obtener todos los domains para análisis manual
    all_domains = domain_service.get_all_domains()
    
    # Análisis manual de datos
    manual_stats = {
        "total_domains": len(all_domains),
        "domains_with_make": len([d for d in all_domains if d.get("make")]),
        "domains_with_model": len([d for d in all_domains if d.get("model")]),
        "domains_with_color": len([d for d in all_domains if d.get("color")]),
        "domains_with_year": len([d for d in all_domains if d.get("year")]),
        "unique_makes": len(set(d.get("make") for d in all_domains if d.get("make"))),
        "year_range": {
            "min": min((d.get("year") for d in all_domains if d.get("year")), default=None),
            "max": max((d.get("year") for d in all_domains if d.get("year")), default=None)
        }
    }
    
    print_result("Análisis manual detallado", manual_stats)
    
    return stats

def test_vehicle_repository_features():
    """Prueba las nuevas características del VehicleRepository"""
    print_separator("PRUEBA 6: Características del VehicleRepository")
    
    with SQLAlchemyUnitOfWork() as uow:
        vehicle_repo = uow.vehicles
        
        # Obtener datos completos de vehículos (límite pequeño)
        vehicles = vehicle_repo.get_vehicle_data(limit=3)
        print_result("Datos completos de vehículos", vehicles)
        
        # Intentar obtener estadísticas de vehículos
        try:
            stats = vehicle_repo.get_vehicle_statistics()
            print_result("Estadísticas de vehículos", stats)
        except Exception as e:
            print(f"⚠️ Error al obtener estadísticas: {e}")
        
        # Buscar vehículo específico por domain (si existe alguno)
        if vehicles:
            first_vehicle = vehicles[0]
            domain_name = first_vehicle.get("domain")
            if domain_name:
                specific_vehicle = vehicle_repo.get_vehicle_by_domain(domain_name)
                print_result(f"Vehículo específico por domain '{domain_name}'", specific_vehicle)
        
        return vehicles

def test_bulk_operations():
    """Prueba las operaciones masivas (bulk)"""
    print_separator("PRUEBA 7: Operaciones Masivas (Bulk)")
    
    domain_service = DomainService()
    
    # Intentar sincronización masiva de fechas
    try:
        sync_dates = domain_service.bulk_update_created_datetime_from_vehicle()
        print_result("Sync masivo de fechas de creación", f"Actualizados: {sync_dates}")
    except Exception as e:
        print(f"⚠️ Error en sync de fechas: {e}")
    
    # Intentar sincronización masiva de campos de vehículo
    try:
        sync_fields = domain_service.bulk_update_vehicle_fields_from_vehicle()
        print_result("Sync masivo de campos de vehículo", f"Actualizados: {sync_fields}")
    except Exception as e:
        print(f"⚠️ Error en sync de campos: {e}")
    
    # Sincronización completa
    try:
        full_sync = domain_service.sync_all_domain_data_from_vehicle()
        print_result("Sincronización completa", full_sync)
    except Exception as e:
        print(f"⚠️ Error en sincronización completa: {e}")

def cleanup_test_data():
    """Limpia los datos de prueba creados"""
    print_separator("LIMPIEZA: Eliminando Datos de Prueba")
    
    domain_service = DomainService()
    
    # Buscar y eliminar domains de prueba
    all_domains = domain_service.get_all_domains()
    test_domains = [d for d in all_domains if d["domain"].startswith("TEST")]
    
    deleted_count = 0
    for domain in test_domains:
        try:
            result = domain_service.delete_domain(domain["id"])
            if result:
                deleted_count += 1
                print(f"✅ Eliminado domain: {domain['domain']}")
        except Exception as e:
            print(f"❌ Error eliminando {domain['domain']}: {e}")
    
    print(f"\n🗑️ Total de domains de prueba eliminados: {deleted_count}")

def main():
    """Función principal que ejecuta todas las pruebas"""
    print("🧪 INICIANDO PRUEBAS COMPLETAS DE FUNCIONALIDADES DE VEHÍCULOS")
    print("="*80)
    
    try:
        # Ejecutar todas las pruebas
        test_domain_creation_with_vehicle_info()
        test_domain_filtering()
        test_domain_updates()
        test_vehicle_service_integration()
        test_domain_statistics()
        test_vehicle_repository_features()
        test_bulk_operations()
        
        # Pregunta si quiere limpiar datos de prueba
        print_separator("¿LIMPIAR DATOS DE PRUEBA?")
        response = input("¿Deseas eliminar los domains de prueba creados? (s/n): ").lower()
        if response == 's':
            cleanup_test_data()
        
        print_separator("✅ PRUEBAS COMPLETADAS EXITOSAMENTE")
        
    except Exception as e:
        print(f"\n❌ ERROR DURANTE LAS PRUEBAS: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()