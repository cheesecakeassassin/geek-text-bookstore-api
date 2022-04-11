from flask import Flask
from app.db import init_db
from app.routes import api
from flask_login import LoginManager
from app.db import get_db
from app.models import AdminUser

def create_app(test_config=None):
  # Set up app config
  app = Flask(__name__, static_url_path='/')
  app.url_map.strict_slashes = False
  app.config.from_mapping(
    SECRET_KEY='super_secret_key'
  )

  login_manager = LoginManager()
  login_manager.init_app(app)
  login_manager.login_view = "login"

  @login_manager.user_loader
  def load_user(admin_id):
    db = get_db;
    return db.query(AdminUser).get(int(admin_id))

  with app.app_context():
    # Import parts of our application
    from app.routes import admin

    app.config['BASIC_AUTH_USERNAME'] = 'sasha'
    app.config['BASIC_AUTH_PASSWORD'] = 'sasha'

    # Register Blueprints
    app.register_blueprint(admin)
    app.register_blueprint(api)

    init_db(app)

  return app