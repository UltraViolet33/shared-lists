from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    IntegerField,
    EmailField,
)
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])