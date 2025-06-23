from core.models.portfolio import Portfolio
from sqlalchemy.exc import SQLAlchemyError

class PortfolioRepository:
    """
    Repositorio para manejar las operaciones CRUD de la tabla portfolio.
    Compatible con sesiones inyectadas (UnitOfWork).
    """

    def __init__(self, session):
        self.session = session

    def get_all_portfolios(self):
        try:
            portfolios = self.session.query(Portfolio).all()
            return [portfolio.to_dict() for portfolio in portfolios]
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener portfolios: {e}")
            return []

    def get_portfolio_by_id(self, portfolio_id):
        try:
            portfolio = self.session.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
            return portfolio.to_dict() if portfolio else None
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener la portfolio con ID {portfolio_id}: {e}")
            return None

    def create_portfolio(self, portfolio_name):
        try:
            new_portfolio = Portfolio(name=portfolio_name)
            self.session.add(new_portfolio)
            self.session.commit()
            print(f"✅ Portfolio creada con ID {new_portfolio.id}")
            return new_portfolio.to_dict()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al crear la portfolio: {e}")
            return None

    def delete_portfolio(self, portfolio_id):
        try:
            portfolio = self.session.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
            if portfolio:
                self.session.delete(portfolio)
                self.session.commit()
                print(f"✅ Portfolio con ID {portfolio_id} eliminada correctamente.")
                return True
            else:
                print(f"⚠️ No se encontró la portfolio con ID {portfolio_id}.")
                return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Error al eliminar la portfolio con ID {portfolio_id}: {e}")
            return False
