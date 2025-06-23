
#from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from core.config.settings import POSTGRES_CONFIG
import pandas as pd

# core/infraestructure/db/postgres.py

class Postgres:
    _instance = None

    def __new__(cls, config=POSTGRES_CONFIG):
        if cls._instance is None:
            cls._instance = super(Postgres, cls).__new__(cls)
            cls._instance.engine = None
            cls._instance.config = config
        return cls._instance

    def connPostgres(self):
        if self.engine:
            return self.engine
        try:
            from sqlalchemy import create_engine
            from sqlalchemy.exc import SQLAlchemyError

            self.engine = create_engine(
                f"postgresql+psycopg2://{self.config['user']}:{self.config['password']}@"
                f"{self.config['host']}:{self.config['port']}/{self.config['dbname']}"
            )
            print("✅ Nueva Conexión a PostgreSQL establecida.")
            return self.engine
        except SQLAlchemyError as e:
            print(f"❌ Error en conexión a PostgreSQL: {e}")
            self.engine = None
            return None



    def query_to_dataframe(self, query):
        """Ejecuta una consulta SQL y devuelve los resultados en un DataFrame de Pandas.
        """
        if not self.engine:
            print("⚠️ No hay una conexión activa a PostgreSQL.")
            return None
        try:
            df = pd.read_sql(query, self.engine)
            return df
        except SQLAlchemyError as e:
            print(f"❌ Error ejecutando la consulta: {e}")
            return None
        """ Ejemplo de uso 
        query = "SELECT * FROM public.portfolio_domain LIMIT 10;"  # Ajusta según tu tabla
        df = db.query_to_dataframe(query)"""