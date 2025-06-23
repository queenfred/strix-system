from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .portfolio import Portfolio
from .domain import Domain

class PortfolioDomain(Base):
    """
    Modelo de la entidad 'PortfolioDomain', que representa la tabla 'public.portfolio_domain'.
    """
    __tablename__ = "portfolio_domain"
    __table_args__ = {"schema": "public"}

    portfolio_id = Column(Integer, ForeignKey("public.portfolio.id", ondelete="CASCADE"), primary_key=True)
    domain_id = Column(Integer, ForeignKey("public.domain.id", ondelete="CASCADE"), primary_key=True)
    state = Column(Boolean, nullable=False, default=True)
    fecha_alta = Column(TIMESTAMP, nullable=False)
    fecha_baja = Column(TIMESTAMP, nullable=True)

    # Relaciones con Portfolio y Domain
    portfolio = relationship(Portfolio, backref="portfolio_domains")
    domain = relationship(Domain, backref="domain_portfolios")

    def __repr__(self):
        return f"<PortfolioDomain(portfolio_id={self.portfolio_id}, domain_id={self.domain_id}, state={self.state}, fecha_alta={self.fecha_alta}, fecha_baja={self.fecha_baja})>"

    def to_dict(self):
        """Convierte la entidad en un diccionario."""
        return {
            "portfolio_id": self.portfolio_id,
            "domain_id": self.domain_id,
            "state": self.state,
            "fecha_alta": self.fecha_alta,
            "fecha_baja": self.fecha_baja
        }