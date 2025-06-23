from sqlalchemy import Column, Integer, String
from .base import Base

class Portfolio(Base):
    """
    Modelo de la entidad 'Portfolio', que representa la tabla 'public.portfolio'.
    """
    __tablename__ = "portfolio"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)

    def __repr__(self):
        return f"<Portfolio(id={self.id}, name='{self.name}')>"

    def to_dict(self):
        """Convierte la entidad en un diccionario."""
        return {
            "id": self.id,
            "name": self.name
        }
