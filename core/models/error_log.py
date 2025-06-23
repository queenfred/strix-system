from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from datetime import datetime
from .base import Base

class ErrorLog(Base):
    """
    Modelo para almacenar logs de errores en la base de datos.
    """
    __tablename__ = "error_log"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(String(255), nullable=False)  # Nombre del método donde ocurrió el error
    error_type = Column(String(255), nullable=False)  # Tipo de error (e.g., NoSuchKey)
    message = Column(Text, nullable=False)  # Mensaje de error detallado
    bucket = Column(String(255), nullable=True)  # Nombre del bucket en S3
    s3_key = Column(Text, nullable=True)  # Clave del archivo en S3
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)  # Timestamp del error

    def to_dict(self):
        return {
            "id": self.id,
            "method": self.method,
            "error_type": self.error_type,
            "message": self.message,
            "bucket": self.bucket,
            "s3_key": self.s3_key,
            "created_at": self.created_at
        }
