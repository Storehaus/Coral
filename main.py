from app import create_app
from config import app_config
from app.broker import Broker

if __name__ == "__main__":
  # some setup
  app_name = app_config.get("APP_NAME", "DefaultAppName")
  print(f"Starting backend for {app_name}")
  
  # Initalize Quart
  app = create_app()

  # Initialize the Broker
  broker = Broker()
  app.broker = broker
  
  # Run Quart
  app.run(host="0.0.0.0", port=7567)