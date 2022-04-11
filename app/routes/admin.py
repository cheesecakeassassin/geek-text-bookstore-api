from flask import Blueprint
from app.models import Admin, Book
from app.db import get_db
from flask import render_template, url_for, redirect
from flask_admin import Admin
from flask_login import login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_basicauth import BasicAuth
from flask_admin.contrib.sqla import ModelView
import bcrypt

bp = Blueprint('admin', __name__, url_prefix='/admin')
salt = bcrypt.gensalt()
admin = Admin(bp, name='microblog', template_mode='bootstrap3')
basic_auth = BasicAuth(bp)
bp.config['BASIC_AUTH_USERNAME'] = 'sasha'
bp.config['BASIC_AUTH_PASSWORD'] = 'sasha'
db = get_db;

login_manager = LoginManager()
login_manager.init_app(bp)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(admin_id):
    db = get_db;
    return db.query(Admin).get(int(admin_id))


admin.add_view(ModelView(Admin, db))
admin.add_view(ModelView(Book, db))
    
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        db = get_db;
        existing_admin_username = db.query(Admin).filter_by(
            username = username.data).first()

        if existing_admin_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")


@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db = get_db;
        user = db.query(Admin).filter_by(username=form.username.data).first()
        if user:
            if bcrypt.checkpw(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('admin.index'))
        else:
            return redirect (url_for('incorrect'))
            return render_template ('incorrect.html')
    return render_template('login.html', form = form)

@bp.route('/incorrect', methods = ['GET', 'POST'])
def incorrect():
    return render_template ('incorrect.html')

@bp.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt)
        new_admin = Admin(username=form.username.data, password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form = form)

@bp.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('dashboard.html')