from app import app, db
from flask import render_template, session, request, flash, url_for, json, Response,redirect, g, make_response
from app.models import UserModel, TicketModel, Assign_ticketModel, CommentModel
from app.forms import NewTicketForm, CommentForm
from werkzeug.security import generate_password_hash, check_password_hash
import random, string,logging, os, flask_sijax, requests
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_sijax import sijax
from urllib.parse import urlparse 



@app.before_request
def before_request_func():
    
    if not request.method == 'GET':
        if not request.path == '/auth/login':
            session= request.cookies.get('session')
            resp=UserModel.decode_auth_token(session)
            if not isinstance(resp, str):
                return redirect("login")
            
            
@app.route("/login")
@app.route("/login.html")
def login():
    return render_template("login.html", title="login")

"""if session.get('Lsession'):
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
         
    return render_template("login.html", title="login", form=form, login=True) """
                            

#FOR FILE UPLOAD
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
@app.route("/index.html")
def index():
    
    return redirect(url_for('login'))

@flask_sijax.route(app,'/dashboard')
def dashboard():
    def getCounts(obj_response,user_Id,role):
        if(role == 'Admin'):
            obj_response.html('#totalT', TicketModel.query.order_by().count())
            obj_response.html('#newT', TicketModel.query.filter_by(status = 'NEW').count())
            obj_response.html('#openT',TicketModel.query.filter_by(status='OPEN').count())
            obj_response.html('#closedT',TicketModel.query.filter_by(status = 'CLOSED').count())
            obj_response.html('#solvedT',TicketModel.query.filter_by(status = 'SOLVED').count())
            obj_response.html('#unsolvedT',TicketModel.query.filter_by(status = 'UNSOLVED').count())
            obj_response.html('#assignedT',TicketModel.query.filter_by(status = 'ASSIGNED').count())
        elif(role == 'Technician'):
            obj_response.html('#totalT', TicketModel.query.filter(Assign_ticketModel.user_id == user_Id).count())
            obj_response.html('#newT', TicketModel.query.filter(Assign_ticketModel.user_id == user_Id , TicketModel.status == 'NEW').count())
            obj_response.html('#openT',TicketModel.query.filter(Assign_ticketModel.user_id == user_Id , TicketModel.status == 'OPEN').count())
            obj_response.html('#closedT',TicketModel.query.filter(Assign_ticketModel.user_id == user_Id , TicketModel.status == 'CLOSED').count())
            obj_response.html('#solvedT',TicketModel.query.filter(Assign_ticketModel.user_id == user_Id , TicketModel.status == 'SOLVED').count())
            obj_response.html('#unsolvedT',TicketModel.query.filter(Assign_ticketModel.user_id == user_Id , TicketModel.status == 'UNSOLVED').count())
            obj_response.html('#assignedT',TicketModel.query.filter(Assign_ticketModel.user_id == user_Id , TicketModel.status == 'UNSOLVED').count())
        elif(role == 'User'):
            obj_response.html('#totalT', TicketModel.query.filter_by(user_id = user_Id).count())
            obj_response.html('#newT', TicketModel.query.filter_by(user_id = user_Id , status ='NEW').count())
            obj_response.html('#openT',TicketModel.query.filter_by(user_id = user_Id , status ='OPEN').count())
            obj_response.html('#closedT',TicketModel.query.filter_by(user_id = user_Id , status = 'CLOSED').count())
            obj_response.html('#solvedT',TicketModel.query.filter_by(user_id = user_Id , status = 'SOLVED').count())
            obj_response.html('#unsolvedT',TicketModel.query.filter_by(user_id = user_Id , status = 'UNSOLVED').count())
            obj_response.html('#assignedT',TicketModel.query.filter_by(user_id = user_Id , status = 'ASSIGNED').count())
            
        
    if g.sijax.is_sijax_request:
        #sijax request detected
        g.sijax.register_callback('getCounts', getCounts)
        return g.sijax.process_request()
    
    return render_template("dashboard.html")
        
        
        

            
# @app.route("/dash/<urlto>/<role>/<userId>")
# def dash(urlto,role,userId):
        
#     if role == 'Admin':
#         data=TicketModel.query.filter_by(status = urlto).all()
#         print(data)
#         return render_template("dash.html", data=data, title=urlto)
#     elif role == 'Technician':
#         data=TicketModel.query.filter(Assign_ticketModel.user_id == userId , TicketModel.status==urlto).all()
#         return render_template("dash.html", data=data, title=urlto)
#     elif session.get('user_role') == 'User':
#         data=TicketModel.query.filter_by(user_id=userId,status=urlto).all()
#         return render_template("dash.html", data=data, title=urlto)
        
        
@app.route("/register")
@app.route("/register.html")
def register():
    
    """ if not session.get('session'):
        return redirect(url_for('login'))
    
    if not session.get('user_role') == 'Admin':
        return redirect(url_for('login'))
    
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
        return redirect(url_for('index')) """
    return render_template("register.html", title="Register")
           
global image  
@app.route("/createticket", methods=['POST','GET'])
def createticket():

    if not request.cookies.get('session'):
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


class Handler(object):
    def __init__(self,ticket_id):
        self.ticket_id=ticket_id
    
    def getTick(self,obj_response):
        datas=TicketModel.query.filter_by(ticketId = self.ticket_id).first()
        assigned =Assign_ticketModel.query.filter_by(ticket_id = self.ticket_id).first()
        if(assigned==None):
            assignedStatus = None
        else:
            assignedStatus = assigned.user.username
                
        obj_response.html("#usrNameD",datas.user.username)
        obj_response.html("#assignedD",assignedStatus)
        obj_response.html("#statusD",datas.status)
        obj_response.html("#priorityD",datas.priority)
        obj_response.html("#updatedD",datas.updated_at.strftime("%d/%m/%y"))
        obj_response.html("#categoryD",datas.category)
        obj_response.html("#subjectD",datas.subject)
        obj_response.html("#createdD",datas.created_at.strftime("%d/%m/%y"))
        obj_response.html("#noteD",datas.comment)
        
    
    def getCom(self,obj_response):
        coms=CommentModel.query.filter_by(ticket_id = self.ticket_id)
        
        for data in coms:
            comment ="""
                <b>%s</b>--><i>%s</i>--><b>%s</b>
                <p>%s</p>
                <hr>
            """%(data.user.username,data.user.role,data.comment_on.strftime("%d/%m/%y"),data.comment)
            print(data.user.username)
            obj_response.html_append('#commentD',comment)
        
    
@flask_sijax.route(app,"/viewticket/<ticket_id>")
def viewticket(ticket_id): 
    
        
    
    if g.sijax.is_sijax_request:
        #sijax request detected
        g.sijax.register_object(Handler(ticket_id))
        return g.sijax.process_request()
    
    #regular (non sijax request)
    return render_template("viewTicket.html" )
    """ form = CommentForm()
    
    comments = CommentModel.query.filter(CommentModel.ticket_id == ticket_id).all()
    
    ticket= TicketModel.query.filter(TicketModel.ticketId  == ticket_id).first()
    
    user= UserModel.query.filter(UserModel.role == 'Technician').all()
    
    #change the status to open
    if session.get('user_role') == 'Admin' and ticket.status == 'NEW':
        ticket.status = 'OPEN'
        ticket.updated_at = datetime.now()
        
        db.session.commit() """
        
    return render_template("viewTicket.html" )


@app.route("/assign", methods=["GET","POST"])
@app.route("/assign/<ticketid>", methods=["GET","POST"])
def assign():
    
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
    global ticket_id,ticketE
    if not session.get('Lsession'):
        return redirect(url_for('login'))
    
    
    if request.method == 'POST':
        comment = request.form.get('comment')
        status = request.form.get('status')
        
        ticket_id = request.form.get('ticket_id')
        user_id = session.get('user_id')
        commentId = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        
        ticketE = TicketModel.query.filter(TicketModel.ticketId  == ticket_id).first()
        
        if status == 'No':
            ticketE.status = 'UNSOLVED'
        elif status== 'Yes' and session.get('user_role')=='Admin':
            ticketE.status = 'CLOSED'
        elif status == 'Yes' and session.get('user_role') == 'Technician':
            ticketE.status = 'SOLVED'
        elif status == 'Yes' and session.get('user_role') == 'User':
            ticketE.status = 'SOLVED' 
               
        new_comment=CommentModel(comment = comment, ticket_id = ticket_id, user_id = user_id, commentId = commentId)
        
        db.session.add(new_comment)
        db.session.commit()
        
    return redirect(f"viewticket/{ticket_id}")


#sijax function
@flask_sijax.route(app,'/hello')
def hello():
    def say_hi(obj_response):
        obj_response.alert("Hi there!")
        
    if g.sijax.is_sijax_request:
        #sijax request detected
        g.sijax.register_callback('say_hi', say_hi)
        return g.sijax.process_request()
    
    #regular (non sijax request)
    return render_template('test.html')

""" @flask_sijax.route(app,'/login')
def login():
    def logger_in(obj_response, username,password):
        data=json.dumps({'username':username,'password':password})
        resp=requests.post('/auth/login',data=data,headers={'Contnet-Type':'application/json','Allow-Method':'POST'})
        
        if resp.status_code != 200:
            obj_response.alert(resp.json())
        else:
            obj_response.alert(resp.json())
        
        if g.sijax.is_sijax_request:
            #sijax request detected
            g.sijax.register_callback('logger_in', logger_in)
            return g.sijax.process_request()
    
        #regular (non sijax request)
        return render_template('login.html') """
        
@app.route('/dash')
@app.route('/dash.html')
def dash():
    return render_template("dash.html")
