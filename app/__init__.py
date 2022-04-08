from flask import Flask
from app.db import init_db
from app.routes import home
from app.routes import home, dashboard

def create_app(test_config=None):
  # Set up app config
  app = Flask(__name__, static_url_path='/')
  app.url_map.strict_slashes = False
  app.config.from_mapping(
    SECRET_KEY='super_secret_key'
  )

  @app.route('/hello')
  def hello():
    return 'hello world!'

  # Register routes
  app.register_blueprint(home)
  app.register_blueprint(dashboard)

  init_db(app)

  return app