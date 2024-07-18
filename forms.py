from flask_wtf import FlaskForm
from wtforms import (
    DecimalField,
    EmailField,
    FloatField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


# Create the neccessary forms for the store, utilising FlaskForm
class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmPassword = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")


# User login parameters
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


# Adding money to user account
class AddFundsForm(FlaskForm):
    amount = FloatField("Amount", validators=[DataRequired()])
    submit = SubmitField("Add Funds")
