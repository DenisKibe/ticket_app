from app import app, db
from flask import render_template, session, request, flash, url_for, json, Response,redirect
from app.models import UserModel, TicketModel, Assign_ticketModel, CommentModel
from app.forms import LoginForm, RegisterForm, NewTicketForm, CommentForm
from werkzeug.security import generate_password_hash, check_password_hash
import random, string,logging, os
from datetime import datetime
from werkzeug.utils import secure_filename

#FOR FILE UPLOAD
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
@app.route("/index.html")
def index():
    
    return redirect("login")

@app.route("/dashboard")
@app.route("/dashboard/<user_Id>")
def dashboard(user_Id):
        if not session.get('Lsession'):
            return redirect(url_for('login'))
        
        user = UserModel.query.filter(UserModel.userId==user_Id).first()
        
        if(user.role == 'Admin'):
            dashboardData = {
                            "totalT" : TicketModel.query.order_by().count(),
                            "newT" : TicketModel.query.filter(TicketModel.status == 'NEW').count(),
                            "openT" : TicketModel.query.filter(TicketModel.status=='OPEN').count(),
                            "closedT" : TicketModel.query.filter(TicketModel.status == 'CLOSED').count(),
                            "solvedT" : TicketModel.query.filter(TicketModel.status == 'SOLVED').count(),
                            "unsolvedT" : TicketModel.query.filter(TicketModel.status == 'UNSOLVED').count(),
                            "assignedT" : TicketModel.query.filter(TicketModel.status == 'ASSIGNED').count(),
                            "unassignedT" : TicketModel.query.filter(TicketModel.status == 'UNASSIGNED').count()
                            }
            return render_template("dashboard.html", dashboardData=dashboardData)
    
        elif(user.role == 'Technician'):
            dashboardData = {
                            "totalT" : Assign_ticketModel.query.filter(Assign_ticketModel.user_id == user_Id).count(),
                            "newT" : Assign_ticketModel.query.filter(Assign_ticketModel.user_id == user_Id , Assign_ticketModel.status == 'NEW').count(),
                            "openT" : Assign_ticketModel.query.filter(Assign_ticketModel.user_id == user_Id , Assign_ticketModel.status == 'OPEN').count(),
                            "closedT" : Assign_ticketModel.query.filter(Assign_ticketModel.user_id == user_Id , Assign_ticketModel.status == 'CLOSED').count(),
                            "solvedT" : Assign_ticketModel.query.filter(Assign_ticketModel.user_id == user_Id , Assign_ticketModel.status == 'SOLVED').count(),
                            "unsolvedT" : Assign_ticketModel.query.filter(Assign_ticketModel.user_id == user_Id , Assign_ticketModel.status == 'UNSOLVED').count(),
                            "assignedT" : Assign_ticketModel.query.filter(Assign_ticketModel.user_id == user_Id , Assign_ticketModel.status == 'ASSIGNED').count(),
                            "unassignedT" : TicketModel.query.filter(TicketModel.user_id == user_Id, TicketModel.status == 'UNASSIGNED').count()
                            }
            return render_template("dashboard.html", dashboardData=dashboardData)
    
        elif(user.role == 'User'):
            dashboardData = {
                            "totalT" : TicketModel.query.filter(TicketModel.user_id == user_Id).count(),
                            "newT" : TicketModel.query.filter(TicketModel.user_id == user_Id , TicketModel.status=='NEW').count(),
                            "openT" : TicketModel.query.filter(TicketModel.user_id == user_Id , TicketModel.status=='OPEN').count(),
                            "closedT" : TicketModel.query.filter(TicketModel.user_id == user_Id , TicketModel.status == 'CLOSED').count(),
                            "solvedT" : TicketModel.query.filter(TicketModel.user_id == user_Id , TicketModel.status == 'SOLVED').count(),
                            "unsolvedT" : TicketModel.query.filter(TicketModel.user_id == user_Id , TicketModel.status == 'UNSOLVED').count(),
                            "assignedT" : TicketModel.query.filter(TicketModel.user_id == user_Id , TicketModel.status == 'ASSIGNED').count(),
                            "unassignedT" : TicketModel.query.filter(TicketModel.user_id == user_Id , TicketModel.status == 'UNASSIGNED').count()
                            }
            return render_template("dashboard.html", dashboardData=dashboardData, user=user)
        
        
        
@app.route("/login", methods=["GET","POST"])
@app.route("/login.html", methods=["GET","POST"])
def login():
    
    if session.get('Lsession'):
        return redirect(f"dashboard/{session.get('user_id')}")
    
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user=UserModel.query.filter(UserModel.email==email).first()
        
        if user is not None:
            if check_password_hash(user.password,password):
                session['Lsession'] = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(64))
                session['user_id']=user.userId
                session['user_role'] = user.role
                session['user_name'] = user.username
                return redirect(f"dashboard/{user.userId}")
            else:
                 return render_template("login.html", title="login", form=form, datax="wrong password", login=True)
        else:
            return render_template("login.html", title="login", form=form, datax='None', login=True)
        
    return render_template("login.html", title="login", form=form, login=True)
            
            
@app.route("/dash/<urlto>")
def dash(urlto=None):
        
        if not session.get('Lsession'):
            return redirect(url_for('login'))
        
        if session.get('user_role') == 'Admin':
            data=TicketModel.query.filter(TicketModel.status == urlto).all()
            return render_template("dash.html", data=data)
        else:
            data=TicketModel.query.filter(TicketModel.userId== session.get('user_id') , TicketModel.status==urlto).all()
            return render_template("dash.html", data=data)
        
        
        
@app.route("/register", methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        passwd=form.password.data
        password = generate_password_hash(passwd)
        email       = form.email.data
        role    = form.role.data
        username  = form.username.data
        userId   = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))

        new_user = UserModel(role=role, email=email, username=username, userId=userId, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("You are successfully registered!","success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form, register=True)
           
global image  
@app.route("/createticket", methods=['POST','GET'])
def createticket():

    if not session.get('Lsession'):
        return redirect(url_for('login'))
    
    form = NewTicketForm()
    if request.method == "POST":
        
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['image']
        
        if file.filename=='':
            flash('No selected file')
        if file and allowed_file(file.filename):
            new_filename = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(7))
            x=file.filename
            y=x.rsplit('.',1)[1]
            
            filename= secure_filename('.'.join([new_filename,y]))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image='/'.join(['/uploads', filename])
            flash('file uploaded')
        
        status = 'NEW'
        comment   = form.comment.data
        category  = form.category.data
        priority  = form.priority.data
        subject  = form.subject.data
        updated_at = datetime.now()
        ticketId   = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        
        new_ticket = TicketModel(user_id=session.get('user_id'),status=status,image=image, comment=comment,category=category, priority=priority, subject=subject,updated_at=updated_at, ticketId=ticketId)
        db.session.add(new_ticket)
        db.session.commit()
        flash("Ticket has been created successfuly","success")
        
        return render_template("createTicket.html", title=category, title2="Image Upload", form=form )
    
    return render_template("createTicket.html", title="Create Ticket", title2="Image Upload", form=form )

@app.route("/viewticket", methods=['POST','GET'])
@app.route("/viewticket/<ticket_id>", methods=['POST','GET'])
def viewticket(ticket_id):
    
    if not session.get('Lsession'):
        return redirect(url_for('login'))
    
    
    
    form = CommentForm()
    
    comments = CommentModel.query.filter(CommentModel.ticket_id == ticket_id).all()
    
    ticket= TicketModel.query.filter(TicketModel.ticketId  == ticket_id).first()
    
    user= UserModel.query.filter(UserModel.role == 'Technician').all()
    
    #change the status to open
    if session.get('user_role') == 'Admin' and ticket.status == 'NEW':
        ticket.status = 'OPEN'
        ticket.updated_at = datetime.now()
        
        db.session.commit()
        
    return render_template("viewTicket.html",ticket = ticket, user=user, form = form, comments=comments )


@app.route("/assign", methods=["GET","POST"])
@app.route("/assign/<ticketid>", methods=["GET","POST"])
def assign(ticketid):
    if not session.get('Lsession'):
        return redirect(url_for('login'))
    
    if request.method == "POST":
        
        user_id = request.form.get('user_id')
        ticket_id = request.form.get('ticket_id')
        assignId   = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        
        new_assign=Assign_ticketModel(user_id=user_id, ticket_id=ticket_id, assignId=assignId, status='ASSIGNED')
        
        db.session.add(new_assign)
        
        ticketE= TicketModel.query.filter(TicketModel.ticketId  == ticket_id).first()
        ticketE.status = 'ASSIGNED'
        ticketE.updated_at = datetime.now()
        
        db.session.commit()
        
        return render_template(f"assign.html",data="done" )
    
@app.route("/comment", methods=["GET","POST"])
def comment():
    global ticket_id
    if not session.get('Lsession'):
        return redirect(url_for('login'))
    
    
    if request.method == 'POST':
        comment = request.form.get('comment')
        
        ticket_id = request.form.get('ticket_id')
        user_id = session.get('user_id')
        commentId = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        
        new_comment=CommentModel(comment = comment, ticket_id = ticket_id, user_id = user_id, commentId = commentId)
        
        db.session.add(new_comment)
        db.session.commit()
        
    return redirect(f"viewticket/{ticket_id}")