# services/audiro/verification_service.py

from sqlalchemy import text



class VerificationService:
    def __init__(self, uow):
        self.uow = uow

    def classify_incidents(self):
        with self.uow:
            repo = self.uow.incidents
            rows = repo.get_incidents_pending_classification()

            if not rows:
                print("No hay incidentes con datos suficientes para clasificar.")
                return

            updated = 0
            for row in rows:
                id_ = row["id"]
                distancia = row["distancia_circulacion"]
                parada = row["parada_zona"]

                # Clasificación basada en umbrales de distancia y parada
                if distancia is None or parada is None:
                    clasificacion = "Sin datos suficientes"
                elif distancia < 0.5 and parada >= 60:
                    clasificacion = "Alta consistencia"
                elif distancia < 1:
                    clasificacion = "Media consistencia"
                else:  # distancia >= 1
                    clasificacion = "Baja consistencia"                    

                repo.update_classification(id_, clasificacion)
                updated += 1

            #self.uow.commit()
            print(f"✅ {updated} incidentes actualizados con clasificación.")

