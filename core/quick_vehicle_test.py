# quick_test.py
"""
Script de pruebas rápidas para funcionalidades específicas de vehículos.
Ejecuta pruebas individuales sin crear datos de prueba.
"""

from core.services.domain_service import DomainService
from core.services.vehicle_service import VehicleService
from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
import json

def test_1_create_single_domain():
    """Prueba rápida: Crear un solo domain con info de vehículo"""
    print("🚗 Creando un domain con información de vehículo...")
    
    domain_service = DomainService()
    
    result = domain_service.create_domain_with_current_datetime(
        domain_name="QUICK_TEST",
        id_thing="mrn:thing:vehicle:quicktest",
        id_account="mrn:account:quicktest",
        subtype="Pickup",
        color="Negro",
        make="Ford",
        model="Ranger",
        year=2023,
        gps="GPS-PREMIUM-X1"
    )
    
    print("✅ Resultado:", json.dumps(result, indent=2, default=str))
    return result

def test_2_get_all_domains():
    """Prueba rápida: Obtener todos los domains y mostrar info de vehículos"""
    print("\n📋 Obteniendo todos los domains...")
    
    domain_service = DomainService()
    domains = domain_service.get_all_domains()
    
    print(f"📊 Total de domains: {len(domains)}")
    
    # Mostrar solo los que tienen información de vehículos
    with_vehicle_info = [d for d in domains if d.get("make")]
    print(f"🚗 Domains con info de vehículo: {len(with_vehicle_info)}")
    
    for domain in with_vehicle_info[:5]:  # Mostrar solo los primeros 5
        print(f"   • {domain['domain']} | {domain.get('make')} {domain.get('model')} ({domain.get('year')}) - {domain.get('color')}")
    
    return len(with_vehicle_info)

def test_3_filter_domains():
    """Prueba rápida: Filtrar domains por marca"""
    print("\n🔍 Filtrando domains por marca...")
    
    domain_service = DomainService()
    
    # Probar diferentes marcas
    marcas_a_probar = ["Toyota", "Ford", "Honda", "Chevrolet", "Volkswagen"]
    
    resultados = {}
    for marca in marcas_a_probar:
        domains = domain_service.get_domains_by_vehicle_criteria(make=marca)
        if domains:
            resultados[marca] = len(domains)
            print(f"   • {marca}: {len(domains)} domains")
    
    if not resultados:
        print("   ⚠️ No se encontraron domains con las marcas probadas")
    
    return resultados

def test_4_get_vehicle_data():
    """Prueba rápida: Obtener datos de strix.vvehicle"""
    print("\n🏭 Obteniendo datos de strix.vvehicle...")
    
    with SQLAlchemyUnitOfWork() as uow:
        vehicles = uow.vehicles.get_vehicle_data(limit=5)
    
    print(f"📊 Vehículos obtenidos: {len(vehicles)}")
    
    for vehicle in vehicles:
        print(f"   • {vehicle.get('domain')} | {vehicle.get('make')} {vehicle.get('model')} ({vehicle.get('year')})")
    
    return vehicles

def test_5_domain_statistics():
    """Prueba rápida: Obtener estadísticas de domains"""
    print("\n📈 Estadísticas de domains...")
    
    domain_service = DomainService()
    stats = domain_service.get_domain_statistics()
    
    print("📊 Estadísticas:")
    for key, value in stats.items():
        print(f"   • {key}: {value}")
    
    return stats

def test_6_sync_sample():
    """Prueba rápida: Intentar sincronización (solo muestra resultado)"""
    print("\n🔄 Probando sincronización...")
    
    domain_service = DomainService()
    
    try:
        # Contar domains sin fecha de creación
        without_date = domain_service.get_domains_with_null_created_datetime()
        print(f"   📅 Domains sin created_datetime: {len(without_date)}")
        
        if len(without_date) > 0:
            print("   ⚠️ Hay domains que podrían necesitar sincronización de fechas")
        else:
            print("   ✅ Todos los domains tienen created_datetime")
            
    except Exception as e:
        print(f"   ❌ Error en sincronización: {e}")

def menu():
    """Menú interactivo para elegir qué probar"""
    opciones = {
        "1": ("Crear domain con info de vehículo", test_1_create_single_domain),
        "2": ("Ver todos los domains", test_2_get_all_domains), 
        "3": ("Filtrar domains por marca", test_3_filter_domains),
        "4": ("Ver datos de strix.vvehicle", test_4_get_vehicle_data),
        "5": ("Ver estadísticas", test_5_domain_statistics),
        "6": ("Probar sincronización", test_6_sync_sample),
        "7": ("Ejecutar todas las pruebas", None)
    }
    
    while True:
        print("\n" + "="*50)
        print("🧪 PRUEBAS RÁPIDAS DE FUNCIONALIDADES")
        print("="*50)
        
        for key, (description, _) in opciones.items():
            print(f"   {key}. {description}")
        print("   0. Salir")
        
        choice = input("\n👉 Elige una opción: ").strip()
        
        if choice == "0":
            print("👋 ¡Hasta luego!")
            break
        elif choice == "7":
            print("🚀 Ejecutando todas las pruebas...")
            for key, (desc, func) in opciones.items():
                if func and key != "7":
                    print(f"\n▶️ {desc}")
                    try:
                        func()
                    except Exception as e:
                        print(f"❌ Error: {e}")
            print("\n✅ Todas las pruebas completadas")
        elif choice in opciones and opciones[choice][1]:
            desc, func = opciones[choice]
            print(f"\n▶️ {desc}")
            try:
                result = func()
                print(f"✅ Prueba completada")
            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("❌ Opción inválida")

def quick_demo():
    """Demo rápido sin menú"""
    print("🚀 DEMO RÁPIDO DE FUNCIONALIDADES")
    print("="*40)
    
    try:
        test_2_get_all_domains()
        test_3_filter_domains() 
        test_5_domain_statistics()
        print("\n✅ Demo completado")
    except Exception as e:
        print(f"❌ Error en demo: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        quick_demo()
    else:
        menu()