from app import app, db, logger
from flask import render_template,  request, flash, url_for,redirect, g
from app.models import UserModel, TicketModel, Assign_ticketModel, CommentModel
import random, string, os, flask_sijax
from datetime import datetime
from werkzeug.utils import secure_filename


#FOR FILE UPLOAD
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
            
@app.route("/login")
@app.route("/login.html")
def login():
    return render_template("login.html", title="login")


@app.route("/")
@app.route("/index.html")
def index():
    
    return redirect(url_for('login'))

@app.route("/dashboard",methods=['POST','GET'])
def dashboard():
    session= request.cookies.get('session')
    resp=UserModel.decode_auth_token(session)
    if not isinstance(resp, str):
        logger.warning('user session: {} --> [{}]'.format(session, resp[1]))
        return redirect(url_for('login'))
    else:
        logger.info('user {} accessing dashboard'.format(resp))
        
#     def getCounts(obj_response,user_Id,role):
#         if(role == 'Admin'):
#             obj_response.html('#totalT', TicketModel.query.order_by().count())
#             obj_response.html('#newT', TicketModel.query.filter_by(status = 'NEW').count())
#             obj_response.html('#closedT',TicketModel.query.filter_by(status = 'CLOSED').count())
#             obj_response.html('#solvedT',TicketModel.query.filter_by(status = 'SOLVED').count())
#             obj_response.html('#unsolvedT',TicketModel.query.filter_by(status = 'UNSOLVED').count())
#             obj_response.html('#assignedT',TicketModel.query.filter_by(status = 'ASSIGNED').count())
            
#         elif(role == 'Technician'):
#             obj_response.html('#totalT', Assign_ticketModel.query.filter_by(user_id = user_Id).count())
#             obj_response.html('#newT', Assign_ticketModel.query.filter_by(user_id = user_Id, status = 'NEW').count())
#             obj_response.html('#assignedT',TicketModel.query.filter_by(user_id = user_Id , status = 'ASSIGNED').count())
#             obj_response.html('#closedT',TicketModel.query.join(Assign_ticketModel, TicketModel.ticketId==Assign_ticketModel.ticket_id).filter(Assign_ticketModel.user_id == user_Id, TicketModel.status=='CLOSED').count())
#             obj_response.html('#solvedT',TicketModel.query.join(Assign_ticketModel, TicketModel.ticketId==Assign_ticketModel.ticket_id).filter(Assign_ticketModel.user_id == user_Id, TicketModel.status=='SOLVED').count())
#             obj_response.html('#unsolvedT',TicketModel.query.join(Assign_ticketModel, TicketModel.ticketId==Assign_ticketModel.ticket_id).filter(Assign_ticketModel.user_id == user_Id, TicketModel.status=='UNSOLVED').count())
            
#         elif(role == 'User'):
#             obj_response.html('#totalT', TicketModel.query.filter_by(user_id = user_Id).count())
#             obj_response.html('#newT', TicketModel.query.filter_by(user_id = user_Id , status ='NEW').count())
#             obj_response.html('#closedT',TicketModel.query.filter_by(user_id = user_Id , status = 'CLOSED').count())
#             obj_response.html('#solvedT',TicketModel.query.filter_by(user_id = user_Id , status = 'SOLVED').count())
#             obj_response.html('#unsolvedT',TicketModel.query.filter_by(user_id = user_Id , status = 'UNSOLVED').count())
#             obj_response.html('#assignedT',TicketModel.query.filter_by(user_id = user_Id , status = 'ASSIGNED').count())
            
        
            
        
#     if g.sijax.is_sijax_request:
#         #sijax request detected
#         g.sijax.register_callback('getCounts', getCounts)
#         return g.sijax.process_request()
    
        return render_template("dashboard.html")
        
@flask_sijax.route(app,'/register')
def register():
    session= request.cookies.get('session')
    resp=UserModel.decode_auth_token(session)
    if not isinstance(resp, str):
        logger.warning('user session: {} --> [{}]'.format(session, resp[1]))
        return redirect(url_for('login'))
    else:
        logger.info('user {} accessing register page'.format(resp))
    
    def validates(obj_response, username):
        datas=UserModel.query.filter_by(username =username).first()
        
        if not datas:
            obj_response.script("$('#LRusername').attr('data-success','available')")
            obj_response.script("$('#Rusername').removeClass('validate').addClass('valid').removeClass('invalid');")
            
        else:
            obj_response.script("$('#LRusername').attr('data-error','Taken!')")
            obj_response.script("$('#Rusername').removeClass('validate').addClass('invalid').removeClass('valid');")
        
    if g.sijax.is_sijax_request:
        #sijax request detected
        g.sijax.register_callback('validates', validates)
        return g.sijax.process_request()
    
    return render_template("register.html", title="Register")
    
class SijaxHandler(object):
    
    @staticmethod
    def _dump_data(obj_response, files, form_values):
        
        def dump_files():
            
            if 'image' not in files:
                logger.warning('No file part')
                return ''

            file_data = files['image']
            file_name = file_data.filename
            
            if file_name is None:
                logger.warning('No selected file')
                return ''

            if file_data and allowed_file(file_name):
                new_filename = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(7))
                fileName=file_data.filename
                ext=fileName.rsplit('.',1)[1]
                filename= secure_filename('.'.join([new_filename,ext]))
                file_data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                imageUrl='/'.join(['/uploads', filename])
                logger.info('uploaded sucessiful')
                return imageUrl
            else:
                logger.warning("no image to upload")
                return ''
        
        imageUrl=dump_files()
        status = 'NEW'
        user_id = form_values.get('userId')
        comment   = form_values.get('description')
        category  = form_values.get('category')
        priority  = form_values.get('priority')
        subject  = form_values.get('subject')
        updated_at = datetime.now()
        ticketId   = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16)) 
       
        
        
        new_ticket = TicketModel(user_id=user_id,status=status,image=imageUrl, comment=comment,category=category, priority=priority, subject=subject,updated_at=updated_at, ticketId=ticketId)
        db.session.add(new_ticket)
        db.session.commit()
       
        obj_response.script("sessionStorage.BtnId='{}';".format(ticketId))
        obj_response.script("window.location='/viewticket.html';")

    @staticmethod
    def start_upload(obj_response, files, form_values):
        SijaxHandler._dump_data(obj_response, files, form_values)

    
@flask_sijax.route(app,"/createticket")
def createticket():
    session= request.cookies.get('session')
    resp=UserModel.decode_auth_token(session)
    if not isinstance(resp, str):
        logger.warning('user session: {} --> [{}]'.format(session, resp[1]))
        return redirect(url_for('login'))
    else:
        logger.info('user {} accessing createticket page'.format(resp))
    
    form_init_js =''
    form_init_js += g.sijax.register_upload_callback('create', SijaxHandler.start_upload)
    
    if g.sijax.is_sijax_request:
        # The request looks like a valid Sijax request
        # The handlers are already registered above.. we can process the request
        return g.sijax.process_request()
    
    return render_template("createTicket.html", title="Create Ticket", title2="Image Upload", form_init_js=form_init_js)


class Handler(object):
     
    @staticmethod
    def clearNew(obj_response,ticket_id):
        ticketA = Assign_ticketModel.query.filter_by(ticket_id = ticket_id, status='NEW').first()
        ticketA.status = "ASSIGNED"
        db.session.commit()
     
    @staticmethod
    def getTick(obj_response,ticket_id):
        datas=TicketModel.query.filter_by(ticketId =ticket_id).first()
        assigned =Assign_ticketModel.query.filter_by(ticket_id =ticket_id).order_by(Assign_ticketModel.assigned_on.desc()).first()
        if(assigned==None):
            assignedStatus = None
        else:
            assignedStatus = assigned.user.username
                    
        obj_response.html("#usrNameD",datas.user.username)
        obj_response.attr("#assignedD",'value',assignedStatus)
        obj_response.html("#opt1",datas.status)
        obj_response.html("#priorityD",datas.priority)
        obj_response.html("#updatedD",datas.updated_at.strftime("%d/%m/%y"))
        obj_response.html("#categoryD",datas.category)
        obj_response.html("#subjectD",datas.subject)
        obj_response.html("#createdD",datas.created_at.strftime("%d/%m/%y"))
        obj_response.html("#noteD",datas.comment)
        obj_response.html("#imgUrl",datas.image)
        
        
        
    @staticmethod
    def getCom(obj_response,ticket_id):
        coms=CommentModel.query.filter_by(ticket_id = ticket_id).order_by(CommentModel.comment_on.desc())
        
        obj_response.html("#commentD",'')
        for data in coms:
            comment ="""\n%s(%s)-->%s\n\n%s\n______________________
            """%(data.user.username,data.user.role,data.comment_on.strftime("%d/%m/%y"),data.comment)
            obj_response.html_append('#commentD',comment)
            
    @staticmethod
    def commenting(obj_response,ticket_id,user_id,comment):
        commentId = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        new_comment=CommentModel(comment = comment, ticket_id = ticket_id, user_id = user_id, commentId = commentId)
        
        db.session.add(new_comment)
        db.session.commit()
        
        
        obj_response.html("#commentD",'')
        Handler.getCom(obj_response,ticket_id)
        
    @staticmethod
    def changeStatus(obj_response,ticket_id,newstatus):
        ticketE = TicketModel.query.filter_by(ticketId = ticket_id).first()
        ticketE.status = newstatus
        ticketE.updated_at = datetime.now()
        
        db.session.commit()
        
    @staticmethod
    def assigning(obj_response,user_id,ticket_id):
        assignId   = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        
        ticketcheck=Assign_ticketModel.query.filter_by(ticket_id=ticket_id,status='NEW').first()
        if ticketcheck:
            Handler.clearNew(obj_response,ticket_id)
        
        new_assign=Assign_ticketModel(user_id=user_id, ticket_id=ticket_id, assignId=assignId, status='NEW')
        db.session.add(new_assign)
        db.session.commit()
        
        Handler.changeStatus(obj_response,ticket_id,"ASSIGNED")
        
    
 
@flask_sijax.route(app,"/viewticket.html")
def viewticket(): 
    session= request.cookies.get('session')
    resp=UserModel.decode_auth_token(session)
    if not isinstance(resp, str):
        logger.warning('user session: {} --> [{}]'.format(session, resp[1]))
        return redirect(url_for('login'))
    else:
        logger.info('user {} accessing viewticket'.format(resp))
    
    if g.sijax.is_sijax_request:
        #sijax request detected
        g.sijax.register_object(Handler)
        return g.sijax.process_request()
    
    #regular (non sijax request)
    return render_template("viewTicket.html" )

@app.route('/dash')
@app.route('/dash.html')
def dash():
    session= request.cookies.get('session')
    resp=UserModel.decode_auth_token(session)
    if not isinstance(resp, str):
        logger.warning('user session: {} --> [{}]'.format(session, resp[1]))
        return redirect(url_for('login'))
    else:
        logger.info('user {} accessing dash'.format(resp))
    
    return render_template("dash.html")
