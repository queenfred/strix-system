from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

class VehicleRepository:
    """
    Repositorio para acceder a la tabla strix.vvehicle en otro esquema de la base de datos.
    """

    def __init__(self, session):
        self.session = session

    def get_vehicle_data(self, domains=None, limit=1):
        """
        Obtiene datos de la tabla strix.vvehicle (id_thing, account_id, domain).
        Si se proporciona una lista de domains, filtra solo esos registros.
        """
        try:
            if domains:
                query = text("""
                    SELECT id AS id_thing, account_id, domain
                    FROM strix.vvehicle
                    WHERE domain IN :domains
                    LIMIT :limit
                """)
                params = {"domains": tuple(domains), "limit": limit}
            else:
                query = text("""
                    SELECT id AS id_thing, account_id, domain
                    FROM strix.vvehicle
                    LIMIT :limit
                """)
                params = {"limit": limit}

            result = self.session.execute(query, params).mappings().all()
            return [dict(row) for row in result]

        except SQLAlchemyError as e:
            print(f"❌ Error al obtener vehículos: {e}")
            return []
