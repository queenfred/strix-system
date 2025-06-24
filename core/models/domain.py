# core/models/domain.py
from sqlalchemy import Column, Integer, String, TIMESTAMP
from .base import Base  # Importación relativa

class Domain(Base):
    """
    Modelo de la entidad 'Domain', que representa la tabla 'public.domain'.
    """
    __tablename__ = "domain"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(String(30), nullable=False)  # Ejemplo: 'AC196QD'
    id_thing = Column(String(100), nullable=True)  # Ejemplo: 'mrn:thing:vehicle:2fd21d42...'
    id_account = Column(String(100), nullable=True)  # Ejemplo: 'mrn:account:6991b4b6...'
    created_datetime = Column(TIMESTAMP, nullable=True)  # 🆕 Nuevo campo agregado

    def __repr__(self):
        return f"<Domain(id={self.id}, domain='{self.domain}', id_thing='{self.id_thing}', id_account='{self.id_account}', created_datetime='{self.created_datetime}')>"

    def to_dict(self):
        """Convierte la entidad en un diccionario."""
        return {
            "id": self.id,
            "domain": self.domain,
            "id_thing": self.id_thing,
            "id_account": self.id_account,
            "created_datetime": self.created_datetime.isoformat() if self.created_datetime else None
        }