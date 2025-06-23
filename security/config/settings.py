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