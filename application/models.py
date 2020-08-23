import flask
from flask import json, Response, jsonify
from application import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Text, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship


class UserModel(db.Model):
  __tablename__='user'
  
  userId = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
  username = db.Column(db.String(80), nullable=False)
  password = db.Column(db.String(200), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  role = db.Column(db.String(30), nullable=False)
  ticketer=relationship("TicketModel", backref='user')
  assigner=relationship("Assign_ticketModel", backref='user')
  commentor=relationship("CommentModel", backref='user')
  
  
  def __init__(self, userId, username,password, email, role):
    self.userId = userId
    self.username = username
    self.password = password
    self.email = email
    self.role = role
    
  def __repr__(self):
    #jdata={'userId':self.userId,'username':self.username,'email':self.email,'role':self.role}
    
    return self.name
  
  
  
class TicketModel(db.Model):
  __tablename__ ='ticket'
  
  user_id = db.Column(db.String(20), ForeignKey('user.userId') , nullable=False)
  ticketId=db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
  status = db.Column(db.String(15), nullable=False)
  image = db.Column(db.String(100), nullable=True)
  comment = db.Column(db.Text)
  category = db.Column(db.String(50))
  priority = db.Column(db.String(50), nullable=False)
  subject = db.Column(db.String(100), nullable=False)
  created_at=db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))
  updated_at = db.Column(db.DateTime)
  assigned=relationship("Assign_ticketModel", backref='ticket')
  commented=relationship("CommentModel", backref='ticket')
  
  def __init__(self,user_id, ticketId,status, image,comment, category,priority, subject, updated_at):
    self.user_id=user_id
    self.ticketId=ticketId 
    self.status=status
    self.image=image
    self.comment=comment
    self.category=category
    self.priority=priority
    self.subject=subject
    self.updated_at= updated_at
    #self.created_at = created_at
    
  def __repr__(self):
  
    #jdata=f"['user':{self.user_id},'ticketId':{self.ticketId},'status':{self.status},'image':{self.image},'comment':{self.comment}],'category':{self.category},'priority':{self.priority},'subject':{self.subject},'created_at':{self.created_at},'updated_at':{self.updated_at}]"
    return self.ticketId
   
   
class Assign_ticketModel(db.Model):
  __tablename__ ='assign_ticket'
  
  assignId = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
  user_id = db.Column(db.String(20), ForeignKey('user.userId') , nullable=False)
  ticket_id = db.Column(db.String(20), ForeignKey('ticket.ticketId') , nullable=False)
  status = db.Column(db.String(15))
  assigned_on = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))
  
  def __init__(self, user_id, ticket_id, assignId, status):
    self.user_id = user_id
    self.ticket_id = ticket_id
    self.assignId = assignId
    self.status = status
    
  def __repr__(self):
    return self.assignId
  
class CommentModel(db.Model):
    __tablename__='comment'
    
    commentId = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.String(20), ForeignKey('user.userId') , nullable=False)
    ticket_id = db.Column(db.String(20), ForeignKey('ticket.ticketId') , nullable=False)
    comment =  db.Column(db.Text)
    comment_on = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))
    
    def __init__(self, commentId, user_id, ticket_id, comment):
      self.commentId = commentId
      self.user_id = user_id
      self.ticket_id = ticket_id
      self.comment = comment
      
    def __repr__(self):
      return self.commentId 