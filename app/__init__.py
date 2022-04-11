from flask import Flask
from app.db import init_db
from app.routes import api, admin

def create_app(test_config=None):
  # Set up app config
  app = Flask(__name__, static_url_path='/')
  app.url_map.strict_slashes = False
  app.config.from_mapping(
    SECRET_KEY='super_secret_key'
  )

  # Register routes
  app.register_blueprint(api)
  app.register_blueprint(admin)

  init_db(app)

  return app