from application import app, db
from flask import render_template, session, request, flash, url_for, json, Response,redirect
from application.models import UserModel, TicketModel
from application.forms import LoginForm, RegisterForm
import random, string

@app.route("/")
@app.route("/index.html")
def index():
    
    return redirect("login")

@app.route("/dashboard/<user_Id>")
def dashboard(user_Id=None):
        if not session.get('Lsession'):
            return redirect(url_for('login'))
        
        user = User.query.filter_by(userId==user_Id).first()
        
        if(user.role == 'Admin'):
            dashboardData = [{
                            "totalT" : Ticket.query.order_by(id).count(),
                            "newT" : Ticket.query.where(status=='New').count(),
                            "closedT" : Ticket.query.where(status == 'Closed').count(),
                            "solvedT" : Ticket.query.where(status == 'Solved').count(),
                            "unsolvedT" : Ticket.query.where(status == 'unsolved').count(),
                            "assignedT" : Ticket.query.where(status == 'Assigned').count(),
                            "unassignedT" : Ticket.query.where(status == 'unassigned').count()
                            }]
            return render_template("dashboard.html", dashboardData=dashboardData)
    
        elif(user.role == 'Technician'):
            dashboardData = [{
                            "totalT" : Ticket.query.filter_by(user_id == user_Id).count(),
                            "newT" : Ticket.query.filter_by(user_id == user_Id).where(status == 'New').count(),
                            "closedT" : Ticket.query.filter_by(user_id == user_Id).where(status == 'Closed').count(),
                            "solvedT" : Ticket.query.filter_by(user_id == user_Id).where(status == 'Solved').count(),
                            "unsolvedT" : Ticket.query.filter_by(user_id == user_Id).where(status == 'unsolved').count(),
                            "assignedT" : Ticket.query.filter_by(user_id == user_Id).where(status == 'Assigned').count(),
                            "unassignedT" : Ticket.query.filter_by(user_id == user_Id).where(status == 'unassigned').count()
                            }]
            return render_template("dashboard.html", dashboardData=dashboardData)
    
        elif(user.role == 'User'):
            dashboardData = [{
                            "totalT" : Ticket.query.filter_by(user_id == user_Id).count(),
                            "closedT" : Ticket.query.filter_by(user_id == user_Id).where(status == 'Closed').count(),
                            "solvedT" : Ticket.query.filter_by(user_id == user_Id).where(status == 'Solved').count(),
                            "unsolvedT" : Ticket.query.filter_by(user_id == user_Id).where(status == 'unsolved').count(),
                            "assignedT" : Ticket.query.filter_by(user_id == user_Id).where(status == 'Assigned').count(),
                            "unassignedT" : Ticket.query.filter_by(user_id == user_Id).where(status == 'unassigned').count()
                            }]
            return render_template("dashboard.html", dashboardData=dashboardData)
        
        
        
@app.route("/login", methods=["GET","POST"])
@app.route("/login.html", methods=["GET","POST"])
def login():
    
    if session.get('Lsession'):
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user=UserModel.query.filter(UserModel.id==2).all()
        
        return render_template("login.html", title="login", form=form, datax=user, login=True)
        
    return render_template("login.html", title="login", form=form, login=True)
            
            
@app.route("/dash/<user_Id>/<urlto>")
def dash(user_Id=None, urlto=None):
        Nuser=User.query.filter_by(userId==user_Id).first()
        if Nuser.role == 'Admin':
            data=Ticket.query.where(status == urlto).all()
            return render_template("/dash", user_Id=user_Id, data=data)
        else:
            data=Ticket.query.filter_by(userId==user_Id).where(status==urlto).all()
            return render_template("/dash", user_Id=user_Id, data=data)
        
@app.route("/register", methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        #user_id     = User.objects.count()
        #user_id     += 1

        email       = form.email.data
        role    = form.role.data
        username  = form.username.data
        userId   = form.userId.data

        new_user = UserModel(id=2,role=role, email=email, username=username, userId=userId)
        db.session.add(new_user)
        db.session.commit()
        flash("You are successfully registered!","success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form, register=True)
           
    
