import os
import io
import fastavro
import pandas as pd
from datetime import datetime
from botocore.exceptions import ClientError
from core.infraestructure.aws.s3 import S3Client
from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork

class S3EventService:
    """
    Servicio para recuperar eventos desde S3 y almacenarlos en la base de datos,
    utilizando UnitOfWork para manejar la transacción.
    """

    def __init__(self):
        self.s3_client = S3Client().conn_s3()

    def retrieve_and_store_events(self, start_date, end_date, domain_id):
        if not self.s3_client:
            with SQLAlchemyUnitOfWork() as uow:
                uow.errors.log_error(
                    method="retrieve_and_store_events",
                    error_type="S3ConnectionFailed",
                    message="No se pudo conectar a S3."
                )
            return "ERROR_S3_CONNECTION"

        with SQLAlchemyUnitOfWork() as uow:
            domain_data = uow.portfolio_domains.get_portfolio_domain_info(domain_id)
            if not domain_data:
                uow.errors.log_error(
                    method="retrieve_and_store_events",
                    error_type="InvalidDomain",
                    message=f"No se encontró información para el domain_id {domain_id}."
                )
                return "INVALID_DOMAIN"

            bucket_name = self.s3_client.config.get('bucket_name')
            file_suffix = self.s3_client.config.get('file_suffix')
            keys_usar = {"event", "latitude", "longitude", "timestamp", "odometer", "speed", "heading"}

            filas = []
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            for dia in pd.date_range(start, end):
                avro_path = (
                    f"ar/magenta/{domain_data['account_id']}/things/type=mrn:things:vehicle/"
                    f"{domain_data['id_thing']}/signals/date="
                    f"{dia.strftime('%Y-%m')}/{dia.strftime('%Y-%m-%d')}{file_suffix}"
                )

                try:
                    response = self.s3_client.s3_client.get_object(Bucket=bucket_name, Key=avro_path)
                    contenido = io.BytesIO(response['Body'].read())
                    reader = fastavro.reader(contenido)
                    for record in reader:
                        filas.append({
                            key: value for key, value in record["details"].items() if key in keys_usar
                        })

                except ClientError as e:
                    uow.errors.log_error(
                        method="retrieve_and_store_events",
                        error_type=e.response['Error']['Code'],
                        message=f"Error al procesar {avro_path}: {e.response['Error']['Message']}",
                        bucket=bucket_name,
                        s3_key=avro_path
                    )

            if filas:
                events_to_store = [
                    {
                        "id_domain": domain_id,
                        "latitude": fila["latitude"],
                        "longitude": fila["longitude"],
                        "speed": fila["speed"],
                        "event": fila["event"],
                        "timestamp": fila["timestamp"],
                        "odometer": fila["odometer"],
                        "heading": fila["heading"]
                    }
                    for fila in filas
                ]
                uow.events.store_events(events_to_store)
                return "SUCCESS"
            else:
                return "NO_EVENTS"
