# Primero importamos librerías necesarias
from unittest.mock import MagicMock
from datetime import datetime, timedelta

# Asumimos que ya tenés importado tu EventProcessingService
# from core.services.event_processing_service import EventProcessingService

# Paso 1 - Creamos mocks para EventService y DomainService
mock_event_service = MagicMock()
mock_domain_service = MagicMock()

# Paso 2 - Creamos una clase de prueba que inyecta los mocks
class TestableEventProcessingService:
    def __init__(self):
        self.event_service = mock_event_service
        self.domain_service = mock_domain_service

    def get_or_process_events(self, id_domain, desde, hasta):
        eventos = self.event_service.get_events_by_domain_and_date(id_domain, desde, hasta)

        if not eventos:
            print(f"⚠️ No se encontraron eventos en la DB para {id_domain}. Procesando...")
            self.domain_service.process_domain_id_events(id_domain, desde, hasta)
            eventos = self.event_service.get_events_by_domain_and_date(id_domain, desde, hasta)
            if not eventos:
                print(f"❌ No se pudieron obtener eventos luego del procesamiento para {id_domain}.")
        
        return eventos

# Paso 3 - Instanciamos el servicio de prueba
service = TestableEventProcessingService()

# Definimos datos de prueba
id_domain = 4873
# Definimos datos de prueba
#fecha = datetime(2024, 11, 17, 4, 59, 10)
timestamp_ms = 1731812350000
desde = datetime.fromtimestamp(timestamp_ms / 1000)
hasta = datetime.now()

# Paso 4 - Configuramos el comportamiento de los mocks

# Simulamos que al principio no hay eventos
mock_event_service.get_events_by_domain_and_date.side_effect = [
    [],  # Primera llamada -> no hay eventos
    [{"id": 1, "id_domain": id_domain, "timestamp": datetime.now()}]  # Segunda llamada -> hay eventos
]

# Paso 5 - Ejecutamos el método que queremos testear
resultados = service.get_or_process_events(id_domain, desde, hasta)

# Paso 6 - Verificamos los resultados
print("\n🎯 Resultados finales:")
print(resultados)

# Paso 7 - Verificamos que se llamaron los métodos esperados
print("\n🛠️ Verificaciones:")
print(f"✔️ Se llamó a get_events_by_domain_and_date (primera vez): {mock_event_service.get_events_by_domain_and_date.call_count >= 1}")
print(f"✔️ Se llamó a process_domain_id_events: {mock_domain_service.process_domain_id_events.called}")
print(f"✔️ Se llamó a get_events_by_domain_and_date (segunda vez): {mock_event_service.get_events_by_domain_and_date.call_count >= 2}")