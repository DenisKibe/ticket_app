from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import UserModel, TicketModel
import email_validator

class LoginForm(FlaskForm):
    email=StringField("Email", validators=[DataRequired(), Email()])
    password=PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    submit=SubmitField("Login")

class RegisterForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired()])
    role = StringField("Role", validators=[DataRequired()])
    username = StringField("userName", validators=[DataRequired()])
    userId = StringField("userId", validators=[DataRequired()])
    submit = SubmitField("Register Now")
