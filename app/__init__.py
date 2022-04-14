from flask import Flask
from app.db import init_db
from app.routes import api as apiRoutes, admin as adminRoutes
from flask_login import LoginManager
from app.db import get_db
from app.models import AdminUser, Book, Author
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_basicauth import BasicAuth

# Initialize app
def create_app(test_config=None):
  # Set up app config
  app = Flask(__name__, static_url_path='/')
  app.url_map.strict_slashes = False
  app.config.from_mapping(
    SECRET_KEY='super_secret_key'
  )

  # Just an extra layer of protection to make sure nothing runs out of context
  with app.app_context():
    # Initialize basic auth for admin routes
    basic_auth = BasicAuth(app)
    app.config['BASIC_AUTH_USERNAME'] = 'sasha'
    app.config['BASIC_AUTH_PASSWORD'] = 'sasha'

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    
    @login_manager.user_loader
    def load_user(admin_id):
      db = get_db();
      return db.query(AdminUser).get(int(admin_id))

    # Import database
    db = get_db()

    # Create admin dashboard using flask_admin import
    admin = Admin(app, name='Geek Text - Bookstore API', template_mode='bootstrap3')
    admin.add_view(ModelView(AdminUser, db))
    admin.add_view(ModelView(Book, db))
    admin.add_view(ModelView(Author, db))

    # Register Blueprints
    app.register_blueprint(adminRoutes)
    app.register_blueprint(apiRoutes)

    # Starts database engine
    init_db(app)

  return app