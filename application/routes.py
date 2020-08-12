from application import app, db
from flask import render_template, session, request, flash, url_for, json, Response
from application.models import User, Ticket
from application.forms import LoginForm
import random, string

@app.route("/")
def index():
    
    return render_template("Llogin.html")

@app.route("/dashboard/<user_id>"):
    def dashboard(user_id=None):
        if not session.get('Lsession'):
            return redirect(url_for('login'))
        
        user = User.query.filter_by(userId=user_id).first();
        
        if(user.role == 'Admin'):
            #some code
        elif(user.role == 'Technician'):
            #some code
        elif(user.role == 'User'):
            some code
        
        
        
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
        
            
    
