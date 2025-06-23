from dotenv import load_dotenv
import os

# Ruta absoluta al .env dentro de core
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

import os

# Minio - Consumer Config
AWS_CONFIG = {
    'ACCESS_KEY': os.getenv('CONSUMER_AVRO_ACCESS_KEY'),
    'SECRET_KEY': os.getenv('CONSUMER_AVRO_SECRET_KEY'),
    'bucket_name': os.getenv('CONSUMER_BUCKET_NAME'),
    'base_path': os.getenv('CONSUMER_BASE_PATH'),
    'file_suffix': os.getenv('CONSUMER_FILE_SUFFIX')
}

# DB - Consumer Config
POSTGRES_CONFIG = {
    'dbname': os.getenv('CONSUMER_DB_NAME'),
    'host': os.getenv('CONSUMER_DB_HOST'),
    'port': os.getenv('CONSUMER_DB_PORT', '5432'),
    'user': os.getenv('CONSUMER_DB_USER'),
    'password': os.getenv('CONSUMER_DB_PASSWORD')
}

# API Keys - External Adapters
GEO_CONFIG = {
    'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
    'OPENCAGE_API_KEY': os.getenv('OPENCAGE_API_KEY'),
    'LOCATIONIQ_API_KEY': os.getenv('LOCATIONIQ_API_KEY'),
    'USER_AGENT': os.getenv('USER_AGENT'),
    'CACHE_FILE': os.getenv('CACHE_FILE')
}

# REPORT INCIDENTS - Config
REPORT_INCIDENT ={
    'S3_AVRO_EVENT': os.getenv('S3_AVRO_EVENT')
}