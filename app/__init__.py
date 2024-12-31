from quart import Quart

from app.broker import Broker
from app.token import TokenManager


def create_app():
  app = Quart("Storehaus-Coral")

  app.broker = Broker()
  app.token_manager = TokenManager() 

  from .routes import bp as routes_bp
  app.register_blueprint(routes_bp)

  return app