from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from app.models import AdminUser
from app.db import get_db

# Handles admin registration for the admin routes
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        db = get_db()
        existing_admin_username = db.query(AdminUser).filter_by(username = username).first()

        if existing_admin_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )