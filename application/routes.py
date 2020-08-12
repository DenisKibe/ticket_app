from application import app
from flask import render_template, session, request, flash, url_for
from application.models import User
from application.forms import LoginForm
import random, string

@app.route("/")
def index():
    if session.get('Lsession'):
        return redirect(url_for('/dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, Welcome")
            session['Lsession'] = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(64))
            return redirect("/dashboard")
        else:
            flash("Sorry, something went wrong.", "danger")
            
    return render_template("Login.html")
