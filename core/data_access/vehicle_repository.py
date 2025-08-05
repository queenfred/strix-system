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
        Obtiene datos completos de la tabla strix.vvehicle incluyendo información del vehículo.
        Si se proporciona una lista de domains, filtra solo esos registros.
        """
        try:
            if domains:
                query = text("""
                    SELECT 
                        id AS id_thing, 
                        account_id, 
                        domain,
                        subtype,
                        color,
                        make,
                        model,
                        year,
                        gps,
                        created_datetime
                    FROM strix.vvehicle
                    WHERE domain IN :domains
                    LIMIT :limit
                """)
                params = {"domains": tuple(domains), "limit": limit}
            else:
                query = text("""
                    SELECT 
                        id AS id_thing, 
                        account_id, 
                        domain,
                        subtype,
                        color,
                        make,
                        model,
                        year,
                        gps,
                        created_datetime
                    FROM strix.vvehicle
                    LIMIT :limit
                """)
                params = {"limit": limit}

            result = self.session.execute(query, params).mappings().all()
            return [dict(row) for row in result]

        except SQLAlchemyError as e:
            print(f"❌ Error al obtener vehículos: {e}")
            return []

    def get_vehicle_basic_data(self, domains=None, limit=1):
        """
        Obtiene solo los datos básicos de la tabla strix.vvehicle (retrocompatibilidad).
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
            print(f"❌ Error al obtener vehículos básicos: {e}")
            return []

    def get_vehicle_by_domain(self, domain_name):
        """
        Obtiene un vehículo específico por su domain.
        """
        try:
            query = text("""
                SELECT 
                    id AS id_thing, 
                    account_id, 
                    domain,
                    subtype,
                    color,
                    make,
                    model,
                    year,
                    gps,
                    created_datetime
                FROM strix.vvehicle
                WHERE domain = :domain_name
                LIMIT 1
            """)
            params = {"domain_name": domain_name}

            result = self.session.execute(query, params).mappings().first()
            return dict(result) if result else None

        except SQLAlchemyError as e:
            print(f"❌ Error al obtener vehículo por domain: {e}")
            return None

    def get_vehicles_by_criteria(self, make=None, model=None, year=None, color=None, limit=1000):
        """
        Obtiene vehículos filtrados por criterios específicos.
        """
        try:
            conditions = []
            params = {"limit": limit}

            if make:
                conditions.append("make = :make")
                params["make"] = make
            if model:
                conditions.append("model = :model")  
                params["model"] = model
            if year:
                conditions.append("year = :year")
                params["year"] = year
            if color:
                conditions.append("color = :color")
                params["color"] = color

            where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

            query = text(f"""
                SELECT 
                    id AS id_thing, 
                    account_id, 
                    domain,
                    subtype,
                    color,
                    make,
                    model,
                    year,
                    gps,
                    created_datetime
                FROM strix.vvehicle
                {where_clause}
                LIMIT :limit
            """)

            result = self.session.execute(query, params).mappings().all()
            return [dict(row) for row in result]

        except SQLAlchemyError as e:
            print(f"❌ Error al obtener vehículos por criterios: {e}")
            return []

    def get_vehicle_statistics(self):
        """
        Obtiene estadísticas básicas de los vehículos.
        """
        try:
            query = text("""
                SELECT 
                    COUNT(*) as total_vehicles,
                    COUNT(DISTINCT make) as unique_makes,
                    COUNT(DISTINCT model) as unique_models,
                    COUNT(DISTINCT color) as unique_colors,
                    MIN(year) as min_year,
                    MAX(year) as max_year,
                    COUNT(DISTINCT account_id) as unique_accounts
                FROM strix.vvehicle
                WHERE domain IS NOT NULL
            """)

            result = self.session.execute(query).mappings().first()
            return dict(result) if result else None

        except SQLAlchemyError as e:
            print(f"❌ Error al obtener estadísticas de vehículos: {e}")
            return None