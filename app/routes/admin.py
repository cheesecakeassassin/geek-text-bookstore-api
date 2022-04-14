from flask import Blueprint, render_template, url_for, redirect
from app.models import AdminUser, LoginForm, RegisterForm
from app.db import get_db
from flask_login import login_user, login_required, logout_user
import bcrypt

# Uses /api endpoint for all of these api routes
bp = Blueprint('admins', __name__, url_prefix='/admins')

# Generates salt used to hash password with bcrypt
salt = bcrypt.gensalt()

# Route for the homepage
@bp.route('/')
def home():
    return render_template('home.html')

# Routes to login with username and password
@bp.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db = get_db();
        user = db.query(AdminUser).filter_by(username=form.username.data).first()
        if user:
            if bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
                login_user(user)
                return redirect(url_for('admin.index'))
        else:
            return redirect (url_for('incorrect'))
    return render_template('login.html', form = form)

# Routes for incorrect login information
@bp.route('/incorrect', methods = ['GET', 'POST'])
def incorrect():
    return render_template ('incorrect.html')

# Routes for registering a new admin user
@bp.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        db = get_db();
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt)
        print(hashed_password)
        new_admin = AdminUser(username=form.username.data, password=hashed_password)
        db.add(new_admin)
        db.commit()
        return redirect(url_for('admins.login'))

    return render_template('register.html', form = form)

# Routes to enter the dashboard
@bp.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

# Routes to logout
@bp.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('dashboard.html')