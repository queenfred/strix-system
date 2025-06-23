from sqlalchemy import Column, BigInteger, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .domain import Domain

class Event(Base):
    """
    Modelo de la entidad 'Event', que representa la tabla 'public.event'.
    """
    __tablename__ = "event"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_domain = Column(Integer, ForeignKey("public.domain.id", ondelete="CASCADE"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed = Column(Float, nullable=False)
    event = Column(Text, nullable=False)
    timestamp = Column(BigInteger, nullable=False)  # 🔹 En milisegundos
    odometer = Column(Float, nullable=False)
    heading = Column(Integer, nullable=False)

    # Relación con Domain
    domain = relationship(Domain, backref="events")

    def __repr__(self):
        return f"<Event(id={self.id}, id_domain={self.id_domain}, laetitude={self.latitude}, longitude={self.longitude}, speed={self.speed}, event='{self.event}', timestamp={self.timestamp}, odometer={self.odometer}, heading={self.heading})>"

    def to_dict(self):
        """Convierte la entidad en un diccionario."""
        return {
            "id": self.id,
            "id_domain": self.id_domain,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "speed": self.speed,
            "event": self.event,
            "timestamp": self.timestamp,  # 🔹 Se mantiene en milisegundos
            "odometer": self.odometer,
            "heading": self.heading
        }
