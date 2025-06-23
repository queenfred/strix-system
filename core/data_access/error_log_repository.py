from core.models.error_log import ErrorLog
from sqlalchemy.exc import SQLAlchemyError

class ErrorLogRepository:
    """
    Repositorio para almacenar logs de errores en la base de datos.
    Requiere una sesión SQLAlchemy inyectada desde UnitOfWork.
    """

    def __init__(self, session):
        self.session = session

    def log_error(self, method, error_type, message, bucket=None, s3_key=None):
        """
        Registra un error en la base de datos.
        """
        try:
            error_entry = ErrorLog(
                method=method,
                error_type=error_type,
                message=message,
                bucket=bucket,
                s3_key=s3_key
            )
            self.session.add(error_entry)
            self.session.commit()
            print(f"🚨 Error registrado en BD: {error_entry.to_dict()}")
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al registrar el log en la base de datos: {e}")
