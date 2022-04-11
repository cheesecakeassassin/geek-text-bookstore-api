from app import db
from flask import Flask
from app.db import init_db
from app.routes import api, admin
from flask_login import LoginManager
from app.db import get_db
from app.models import AdminUser, Book
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_basicauth import BasicAuth

def create_app(test_config=None):
  # Set up app config
  app = Flask(__name__, static_url_path='/')
  app.url_map.strict_slashes = False
  app.config.from_mapping(
    SECRET_KEY='super_secret_key'
  )
  with app.app_context():
    basic_auth = BasicAuth(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    app.config['BASIC_AUTH_USERNAME'] = 'sasha'
    app.config['BASIC_AUTH_PASSWORD'] = 'sasha'

    @login_manager.user_loader
    def load_user(admin_id):
      db = get_db();
      return db.query(AdminUser).get(int(admin_id))

    db = get_db()

    adminb = Admin(app, name='microblog', template_mode='bootstrap3')
    adminb.add_view(ModelView(AdminUser, db))
    adminb.add_view(ModelView(Book, db))

    # Register Blueprints
    app.register_blueprint(admin)
    app.register_blueprint(api)

    init_db(app)

  return app