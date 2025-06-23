import logging
from sqlalchemy import text

from core.infraestructure.aws.s3 import S3Client
from core.infraestructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

def health_check():
    """
    Realiza el chequeo de salud de PostgreSQL y S3 usando Unit of Work para DB.
    """
    status = {"postgres": "FAIL", "s3": "FAIL"}

    # PostgreSQL usando Unit of Work
    try:
        with SQLAlchemyUnitOfWork() as uow:
            uow.session.execute(text("SELECT 1"))
            status["postgres"] = "OK"
            logger.info("✅ PostgreSQL está operativo.")
    except Exception as e:
        logger.error(f"❌ Error en la conexión a PostgreSQL: {e}")

    # Chequeo de S3
    try:
        s3_client = S3Client()
        client = s3_client.conn_s3()
        if client:
            status["s3"] = "OK"
            logger.info("✅ S3 está operativo.")
        else:
            logger.warning("❌ S3 no está disponible.")
    except Exception as e:
        logger.error(f"❌ Error en la conexión a S3: {e}")

    return status
