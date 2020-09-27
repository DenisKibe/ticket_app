from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import UserModel, TicketModel
import email_validator 

class LoginForm(FlaskForm):
    email=StringField("Email", validators=[DataRequired(), Email()])
    password=PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    submit=SubmitField("Login")

class RegisterForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired()])
    role = SelectField("Role",choices=['User','Technician','Admin'], validators=[DataRequired()])
    username = StringField("userName", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register Now")
    
class NewTicketForm(FlaskForm):
    status = StringField("Status", validators=[DataRequired()])
    comment = TextAreaField("Comment", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    priority = SelectField("Priority",choices=['LOW','MEDIUM','HIGH'], validators=[DataRequired()])
    subject = StringField("Subject", validators=[DataRequired()])
    image = FileField("Image")
    
    submitT = SubmitField("Create New")
    
class CommentForm(FlaskForm):
    comment = TextAreaField("comment", validators=[DataRequired()])
    status = SelectField('Solved', choices=[('Yes'),('No')])
    
    submit = SubmitField("Post") 
