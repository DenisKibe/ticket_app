import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from SQLAlchemy import Column, Integer, String, Float

class User(db.Model):
  id= db.Column(db.Integer)
  userId = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
  username = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  role = db.Column(db.String(30), nullable=False)
  
  
 class Ticket(db.Model):
  user_id = db.Column(db.String(20), db.foreignKey('User.userId'), nullable=False)
  id = db.Column(db.Integer)
  ticketId=db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
  status = db.Column(db.String(15), nullable=False)
  image = db.Column(db.String(100), nullable=True)
  comment = db.Column(db.Text)
  category = db.Column(db.String(50))
  priority = db.Column(db.String(50), nullable=False)
  subject = db.Column(db.String(100), nullable=False)
  
