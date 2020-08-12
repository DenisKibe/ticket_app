from application import app, db
from flask import render_template, session, request, flash, url_for, json, Response
from application.models import User, Ticket
from application.forms import LoginForm
import random, string

@app.route("/")
def index():
    
    return render_template("login.html")

@app.route("/dashboard/<user_Id>"):
    def dashboard(user_Id=None):
        if not session.get('Lsession'):
            return redirect(url_for('login'))
        
        user = User.query.filter_by(userId==user_Id).first();
        
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
        
        
        
@app.route("/login"):
    if session.get('Lsession'):
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, Welcome")
            session['Lsession'] = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(64))
            return redirect("dashboard")
        else:
            flash("Sorry, something went wrong.", "danger")
            
            
@app.route("/<user>/<urlto>"):
    def urlto(user=None, urlto=None):
        
            
    
