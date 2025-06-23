from core.models.portfolio_domain import PortfolioDomain
from core.models.portfolio import Portfolio
from core.models.domain import Domain
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class PortfolioDomainRepository:
    """
    Repositorio para manejar las operaciones CRUD de la tabla portfolio_domain.
    """

    def __init__(self, session):
        self.session = session

    def get_portfolio_domain_details(self, portfolio_id, domain_id):
        try:
            result = self.session.query(
                Portfolio.name.label("portfolio_name"),
                Domain.domain.label("domain_name"),
                Domain.id_thing,
                Domain.id_account,
                PortfolioDomain.state,
                PortfolioDomain.fecha_alta,
                PortfolioDomain.fecha_baja
            ).join(Portfolio, Portfolio.id == PortfolioDomain.portfolio_id) \
             .join(Domain, Domain.id == PortfolioDomain.domain_id) \
             .filter(PortfolioDomain.portfolio_id == portfolio_id,
                     PortfolioDomain.domain_id == domain_id,
                     PortfolioDomain.state == True).first()

            if result:
                return {
                    "portfolio_name": result.portfolio_name,
                    "domain_name": result.domain_name,
                    "id_thing": result.id_thing,
                    "id_account": result.id_account,
                    "state": result.state,
                    "fecha_alta": result.fecha_alta.strftime("%Y-%m-%d %H:%M:%S") if result.fecha_alta else None,
                    "fecha_baja": result.fecha_baja.strftime("%Y-%m-%d %H:%M:%S") if result.fecha_baja else None
                }
            else:
                return None
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener detalles de Portfolio-Domain: {e}")
            return None

    def portfolio_domain_exists(self, portfolio_id, domain_id):
        return self.session.query(PortfolioDomain).filter(
            PortfolioDomain.portfolio_id == portfolio_id,
            PortfolioDomain.domain_id == domain_id
        ).first() is not None

    def create_portfolio_domain(self, portfolio_id, domain_id, state=True, fecha_baja=None):
        try:
            portfolio = self.session.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
            domain = self.session.query(Domain).filter(Domain.id == domain_id).first()

            if not portfolio or not domain:
                return None

            if self.portfolio_domain_exists(portfolio_id, domain_id):
                return None

            new_portfolio_domain = PortfolioDomain(
                portfolio_id=portfolio_id,
                domain_id=domain_id,
                state=state,
                fecha_alta=datetime.utcnow(),
                fecha_baja=fecha_baja
            )
            self.session.add(new_portfolio_domain)
            self.session.commit()
            return new_portfolio_domain.to_dict()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al crear Portfolio-Domain: {e}")
            return None

    def get_all_portfolio_domains(self):
        try:
            results = self.session.query(
                PortfolioDomain.portfolio_id,
                PortfolioDomain.domain_id,
                Portfolio.name.label("portfolio_name"),
                Domain.domain.label("domain_name"),
                Domain.id_thing,
                Domain.id_account,
                PortfolioDomain.state,
                PortfolioDomain.fecha_alta,
                PortfolioDomain.fecha_baja
            ).join(Portfolio, Portfolio.id == PortfolioDomain.portfolio_id) \
             .join(Domain, Domain.id == PortfolioDomain.domain_id) \
             .filter(PortfolioDomain.state == True).all()

            return [
                {
                    "portfolio_id": result.portfolio_id,
                    "domain_id": result.domain_id,
                    "portfolio_name": result.portfolio_name,
                    "domain_name": result.domain_name,
                    "id_thing": result.id_thing,
                    "id_account": result.id_account,
                    "state": result.state,
                    "fecha_alta": result.fecha_alta.strftime("%Y-%m-%d %H:%M:%S") if result.fecha_alta else None,
                    "fecha_baja": result.fecha_baja.strftime("%Y-%m-%d %H:%M:%S") if result.fecha_baja else None
                }
                for result in results
            ]
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener todas las relaciones Portfolio-Domain activas: {e}")
            return []

    def get_portfolio_domain(self, portfolio_id, domain_id):
        try:
            portfolio_domain = self.session.query(PortfolioDomain).filter(
                PortfolioDomain.portfolio_id == portfolio_id,
                PortfolioDomain.domain_id == domain_id,
                PortfolioDomain.state == True
            ).first()
            return portfolio_domain.to_dict() if portfolio_domain else None
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener Portfolio-Domain: {e}")
            return None

    def delete_portfolio_domain(self, portfolio_id, domain_id):
        try:
            portfolio_domain = self.session.query(PortfolioDomain).filter(
                PortfolioDomain.portfolio_id == portfolio_id,
                PortfolioDomain.domain_id == domain_id,
                PortfolioDomain.state == True
            ).first()
            if not portfolio_domain:
                return False

            portfolio_domain.state = False
            portfolio_domain.fecha_baja = datetime.utcnow()
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al borrar lógicamente Portfolio-Domain: {e}")
            return False

    def delete_fisico_portfolio_domain(self, portfolio_id, domain_id):
        try:
            portfolio_domain = self.session.query(PortfolioDomain).filter(
                PortfolioDomain.portfolio_id == portfolio_id,
                PortfolioDomain.domain_id == domain_id
            ).first()
            if not portfolio_domain:
                return False

            self.session.delete(portfolio_domain)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al borrar Portfolio-Domain: {e}")
            return False

    def get_domains_by_portfolio(self, portfolio_id):
        try:
            domain_ids = self.session.query(PortfolioDomain.domain_id).filter_by(
                portfolio_id=portfolio_id, state=True).all()
            return [d[0] for d in domain_ids]
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener los dominios del portfolio: {e}")
            return []

    def get_portfolio_domain_info(self, domain_id):
        try:
            result = self.session.query(Domain.id_account, Domain.id_thing).filter(
                Domain.id == domain_id).first()
            if result:
                return {
                    "account_id": result.id_account,
                    "id_thing": result.id_thing
                }
            return None
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener información de dominio: {e}")
            return None

    def get_active_portfolios(self):
        try:
            active_portfolios = self.session.query(PortfolioDomain.portfolio_id).filter_by(
                state=True).distinct().all()
            return [p[0] for p in active_portfolios]
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener los portfolios activos: {e}")
            return []
