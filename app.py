from flask import Flask, render_template, url_for, redirect
from flask_admin import Admin, BaseView, expose
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_basicauth import BasicAuth
from flask_admin.contrib.sqla import ModelView



app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
admin = Admin(app, name='microblog', template_mode='bootstrap3')
basic_auth = BasicAuth(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['BASIC_AUTH_USERNAME'] = 'sasha'
app.config['BASIC_AUTH_PASSWORD'] = 'sasha'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique = True)
    password = db.Column(db.String(80), nullable=False)

class Add(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(30), nullable = False, unique = True)
    isbn = db.Column(db.Integer, nullable = False, unique = True)
    author = db.Column(db.String(20), nullable = False)
    publisher = db.Column(db.String(20), nullable = False)
    genre = db.Column(db.String(20), nullable = False)
    price = db.Column(db.Float, nullable = False)
    year = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String(20), nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    sold = db.Column(db.Integer, nullable = False)

class Cards(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable = False)
    card_number = db.Column(db.Integer, nullable = False, unique = True)
    expiration_date = db.Column(db.Integer, nullable = False)
    security_code = db.Column(db.Integer, nullable = False)
    zip_code = db.Column(db.Integer, nullable = False)


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Add, db.session))
    
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username = username.data).first()

        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('admin.index'))
        else:
            return redirect (url_for('incorrect'))
            return render_template ('incorrect.html')
    return render_template('login.html', form = form)

@app.route('/incorrect', methods = ['GET', 'POST'])
def incorrect():
    return render_template ('incorrect.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form = form)

@app.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug = True)
    app.run(host="0.0.0.0")

