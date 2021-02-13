from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app import logger
from app.models import CommentModel, TicketModel, Assign_ticketModel, UserModel
import datetime

api_blueprint = Blueprint('api', __name__)


class GetDataApi(MethodView):
    """
    get data resource
    """
    def post(self):
        user_Id=UserModel.verify_auth_header(request.headers.get('Authorization'))
        if not isinstance(user_Id, str):
            return make_response(jsonify({'message':'failed'})), 401
        else:
            logger.info('user {} accessing  /api/getdata'.format(user_Id))
            #get data from the user
            post_data = request.get_json()
            responseBody=[]
            if post_data.get('role') == 'Admin':
                try:
                    datas=TicketModel.query.filter_by(status = post_data.get('status')).order_by(TicketModel.updated_at.desc())
                
                    #create a dict of results
                    numCount = 0
                    for data in datas:
                        numCount+=1
                        respObject={
                            'numCount': numCount,
                            'ticketId' : data.ticketId,
                            'username':data.user.username,
                            'subject' : data.subject,
                            'category' : data.category,
                            'priority' : data.priority,
                            'status' : data.status,
                            'created' : data.created_at.strftime("%d/%m/%y"),
                            'updated' : data.updated_at.strftime("%d/%m/%y")
                        }
                        responseBody.append(respObject)
                    
                    return make_response(jsonify(responseBody)),200
                except Exception as e:
                    print(e)
                    responseObject = {
                        'status': 'fail',
                        'message' : 'Try again'
                    }
                    return make_response(jsonify(responseObject)), 500
                
            elif post_data.get('role') == 'Technician':
                if post_data.get('status') == 'NEW':
                    try:
                        datas=Assign_ticketModel.query.filter_by(status = post_data.get('status'), user_id = user_Id).order_by(Assign_ticketModel.assigned_on.desc())
                        
                        #create a dict of results
                        numCount = 0
                        for data in datas:
                            numCount+=1
                            respObject={
                                'numCount':numCount,
                                'username':data.user.username,
                                'ticketId' : data.ticket_id,
                                'status' : data.ticket.status,
                                'category' : data.ticket.category,
                                'priority' : data.ticket.priority,
                                'subject' : data.ticket.subject,
                                'created' : data.ticket.created_at.strftime("%d/%m/%y"),
                                'updated' : data.ticket.updated_at.strftime("%d/%m/%y")
                            }
                            responseBody.append(respObject)
                        
                        return make_response(jsonify(responseBody)),200
                    except Exception as e:
                        print(e)
                        responseObject = {
                            'status': 'fail',
                            'message' : 'Try again'
                        }
                        return make_response(jsonify(responseObject)), 500
                    
                elif post_data.get('status') == 'ASSIGNED':
                    try:
                        datas=TicketModel.query.filter_by(status = post_data.get('status'), user_id = user_Id).order_by(TicketModel.updated_at.desc())
                        
                        #create a dict of results
                        numCount = 0
                        for data in datas:
                            numCount+=1
                            respObject={
                                'numCount':numCount,
                                'username':data.user.username,
                                'ticketId' : data.ticketId,
                                'status' : data.status,
                                'category' : data.category,
                                'priority' : data.priority,
                                'subject' : data.subject,
                                'created' : data.created_at.strftime("%d/%m/%y"),
                                'updated' : data.updated_at.strftime("%d/%m/%y")
                            }
                            responseBody.append(respObject)
                        
                        return make_response(jsonify(responseBody)),200
                    except Exception as e:
                        print(e)
                        responseObject = {
                            'status': 'fail',
                            'message' : 'Try again'
                        }
                        return make_response(jsonify(responseObject)), 500
                    
                else:
                    try:
                        datas=TicketModel.query.join(Assign_ticketModel, TicketModel.ticketId==Assign_ticketModel.ticket_id).filter(Assign_ticketModel.user_id == user_Id, TicketModel.status==post_data.get('status')).order_by(TicketModel.updated_at.desc())
                        
                        #create a dict of results
                        numCount = 0
                        for data in datas:
                            numCount+=1
                            respObject={
                                'numCount': numCount,
                                'username':data.user.username,
                                'ticketId' : data.ticketId,
                                'status' : data.status,
                                'category' : data.category,
                                'priority' : data.priority,
                                'subject' : data.subject,
                                'created' : data.created_at.strftime("%d/%m/%y"),
                                'updated' : data.updated_at.strftime("%d/%m/%y")
                            }
                            responseBody.append(respObject)
                        
                        return make_response(jsonify(responseBody)),200
                    except Exception as e:
                        print(e)
                        responseObject = {
                            'status': 'fail',
                            'message' : 'Try again'
                        }
                        return make_response(jsonify(responseObject)), 500
                    
            elif post_data.get('role') == 'User':
                try:
                    datas=TicketModel.query.filter_by(status = post_data.get('status'), user_id = user_Id).order_by(TicketModel.updated_at.desc())
                
                    #create a dict of results
                    numCount = 0
                    for data in datas:
                        numCount+=1
                        respObject={
                            'numCount':numCount,
                            'username':data.user.username,
                            'ticketId' : data.ticketId,
                            'status' : data.status,
                            'category' : data.category,
                            'priority' : data.priority,
                            'subject' : data.subject,
                            'created' : data.created_at.strftime("%d/%m/%y"),
                            'updated' : data.updated_at.strftime("%d/%m/%y")
                        }
                        responseBody.append(respObject)
                    
                    return make_response(jsonify(responseBody)),200
                except Exception as e:
                    print(e)
                    responseObject = {
                        'status': 'fail',
                        'message' : 'Try again'
                    }
                    return make_response(jsonify(responseObject)), 500
        
        
class GetTicketAPI(MethodView):
    """get ticket based on ID """
    def post(self):
        user_Id=UserModel.verify_auth_header(request.headers.get('Authorization'))
        if not isinstance(user_Id, str):
            logger.warning('user session {} -->[{}]'.format(request.headers.get('Authorization'), user_Id[1]))
            return make_response(jsonify({'message':'failed'})), 401
        else:
            logger.info('user {} accessing  /api/getticket'.format(user_Id))
            post_data = request.get_json()
            
            try:
                datas=TicketModel.query.filter_by(ticketId = post_data.get('ticketId')).first()
                assigned =Assign_ticketModel.query.filter_by(ticket_id = post_data.get('ticketId')).first()
                if(assigned==None):
                    assignedStatus = None
                else:
                    assignedStatus = assigned.user.username
                    
                    #return data
                respObject={
                    'username':datas.user.username,
                    'ticketId' : datas.ticketId,
                    'status' : datas.status,
                    'imageURL' : datas.image,
                    'category' : datas.category,
                    'comment' : datas.comment,
                    'priority' : datas.priority,
                    'subject' : datas.subject,
                    'created' : datas.created_at.strftime("%d/%m/%y"),
                    'updated' : datas.updated_at.strftime("%d/%m/%y"),
                    'Assigned' : assignedStatus
                }
                print(respObject)
                return make_response(jsonify(respObject)),200
            except Exception as e:
                print(e)
                responseObject = {
                    'status': 'fail',
                    'message' : 'Try again'
                }
                return make_response(jsonify(responseObject)), 500
 
class SearchAPI(MethodView):
     """
     search any field of ticket
     """
     def post(self):
        user_Id=UserModel.verify_auth_header(request.headers.get('Authorization'))
        if not isinstance(user_Id, str):
            logger.warning('user session {} -->[{}]'.format(request.headers.get('Authorization'), user_Id[1]))
            return make_response(jsonify({'message':'failed'})), 401
        else:
            logger.info('user {} accessing  /api/search'.format(user_Id))
            post_data = request.get_json()
            responseBody=[]
            
            if post_data.get('field') == 'subject':
                
                try:
                    if post_data.get('role') == 'Admin':
                        datas= TicketModel.query.filter(TicketModel.subject.like('%'+post_data.get('vall')+'%')).order_by(TicketModel.updated_at.desc())
                    elif post_data.get('role') == 'User':
                        datas= TicketModel.query.filter(TicketModel.user_id == user_Id ,TicketModel.subject.like('%'+post_data.get('vall')+'%')).order_by(TicketModel.updated_at.desc())
                    elif post_data.get('role') == 'Technician':
                        datas=TicketModel.query.join(Assign_ticketModel, TicketModel.ticketId==Assign_ticketModel.ticket_id).filter(Assign_ticketModel.user_id == user_Id, TicketModel.subject.like('%'+post_data.get('vall')+'%')).order_by(TicketModel.updated_at.desc())
                        
                    for data in datas:
                        respObject={
                            'username':data.user.username,
                            'ticketId' : data.ticketId,
                            'status' : data.status,
                            'imageURL' : data.image,
                            'category' : data.category,
                            'priority' : data.priority,
                            'subject' : data.subject,
                            'created' : data.created_at.strftime("%d/%m/%y"),
                            'updated' : data.updated_at.strftime("%d/%m/%y")
                        }
                        responseBody.append(respObject)
                    
                    return make_response(jsonify(responseBody)),200
                except Exception as e:
                    print(e)
                    responseObject = {
                        'status': 'fail',
                        'message' : 'Try again'
                    }
                    return make_response(jsonify(responseObject)), 500
                
            elif post_data.get('field') == 'comment':
                
                try:
                    if post_data.get('role') == 'Admin':
                        datas= TicketModel.query.filter(TicketModel.comment.like('%'+post_data.get('vall')+'%')).order_by(TicketModel.updated_at.desc())
                    elif post_data.get('role') == 'User':
                        datas= TicketModel.query.filter(TicketModel.user_id == user_Id,TicketModel.comment.like('%'+post_data.get('vall')+'%')).order_by(TicketModel.updated_at.desc())
                    elif post_data.get('role') == 'Technician':
                        datas=TicketModel.query.join(Assign_ticketModel, TicketModel.ticketId==Assign_ticketModel.ticket_id).filter(Assign_ticketModel.user_id == user_Id, TicketModel.comment.like('%'+post_data.get('vall')+'%')).order_by(TicketModel.updated_at.desc())
                        
                    for data in datas:
                        respObject={
                            'username':data.user.username,
                            'ticketId' : data.ticketId,
                            'status' : data.status,
                            'imageURL' : data.image,
                            'category' : data.category,
                            'priority' : data.priority,
                            'subject' : data.subject,
                            'created' : data.created_at.strftime("%d/%m/%y"),
                            'updated' : data.updated_at.strftime("%d/%m/%y")
                        }
                        responseBody.append(respObject)
                    
                    return make_response(jsonify(responseBody)),200
                except Exception as e:
                    print(e)
                    responseObject = {
                        'status': 'fail',
                        'message' : 'Try again'
                    }
                    return make_response(jsonify(responseObject)), 500
                
            elif post_data.get('field') == 'category':
                
                try:
                    if post_data.get('role') == 'Admin':
                        datas= TicketModel.query.filter(TicketModel.category.like('%'+post_data.get('vall')+'%')).order_by(TicketModel.updated_at.desc())
                    elif post_data.get('role') == 'User':
                        datas= TicketModel.query.filter(TicketModel.user_id == user_Id,TicketModel.category.like('%'+post_data.get('vall')+'%')).order_by(TicketModel.updated_at.desc())
                    elif post_data.get('role') == 'Technician':
                        datas=TicketModel.query.join(Assign_ticketModel, TicketModel.ticketId==Assign_ticketModel.ticket_id).filter(Assign_ticketModel.user_id == user_Id, TicketModel.category.like('%'+post_data.get('vall')+'%')).order_by(TicketModel.updated_at.desc())
                    for data in datas:
                        respObject={
                            'username':data.user.username,
                            'ticketId' : data.ticketId,
                            'status' : data.status,
                            'imageURL' : data.image,
                            'category' : data.category,
                            'priority' : data.priority,
                            'subject' : data.subject,
                            'created' : data.created_at.strftime("%d/%m/%y"),
                            'updated' : data.updated_at.strftime("%d/%m/%y")
                        }
                        responseBody.append(respObject)
                    
                    return make_response(jsonify(responseBody)),200
                except Exception as e:
                    print(e)
                    responseObject = {
                        'status': 'fail',
                        'message' : 'Try again'
                    }
                    return make_response(jsonify(responseObject)), 500
                
            elif post_data.get('field') == 'ID':
                
                try:
                    if post_data.get('role') == 'Admin':
                        datas= TicketModel.query.filter(TicketModel.ticketId.like('%'+post_data.get('vall')+'%')).order_by(TicketModel.updated_at.desc())
                    elif post_data.get('role')=='User':
                        datas= TicketModel.query.filter(TicketModel.user_id == user_Id,TicketModel.ticketId.like('%'+post_data.get('vall')+'%')).order_by(TicketModel.updated_at.desc())
                    elif post_data.get('role')=='Technician':
                        datas=TicketModel.query.join(Assign_ticketModel, TicketModel.ticketId==Assign_ticketModel.ticket_id).filter(Assign_ticketModel.user_id == user_Id, TicketModel.ticketId.like('%'+post_data.get('vall')+'%')).order_by(TicketModel.updated_at.desc())

                    for data in datas:
                        respObject={
                            'username':data.user.username,
                            'ticketId' : data.ticketId,
                            'status' : data.status,
                            'imageURL' : data.image,
                            'category' : data.category,
                            'priority' : data.priority,
                            'subject' : data.subject,
                            'created' : data.created_at.strftime("%d/%m/%y"),
                            'updated' : data.updated_at.strftime("%d/%m/%y")
                        }
                        responseBody.append(respObject)
                    
                    return make_response(jsonify(responseBody)),200
                except Exception as e:
                    print(e)
                    responseObject = {
                        'status': 'fail',
                        'message' : 'Try again'
                    }
                    return make_response(jsonify(responseObject)), 500
                
class GetListTechAPI(MethodView):
    """get list of Techs and their ID """
    def get(self):
        user_Id=UserModel.verify_auth_header(request.headers.get('Authorization'))
        if not isinstance(user_Id, str):
            logger.warning('user session {} -->[{}]'.format(request.headers.get('Authorization'), user_Id[1]))
            return make_response(jsonify({'message':'failed'})), 401
        else:
            logger.info('user {} accessing  /api/getlisttech'.format(user_Id))
            responseBody=[]
            data= UserModel.query.filter_by(role='Technician')
            for techs in data:
                respObject={
                    'username':techs.username,
                    'user_id':techs.userId
                }
                responseBody.append(respObject)
            
            return make_response(jsonify(responseBody)),200
        
class GetStatsAPI(MethodView):
    """get stats  """
    def get(self):
        user_Id=UserModel.verify_auth_header(request.headers.get('Authorization'))
        if not isinstance(user_Id, str):
            logger.warning('user session {} -->[{}]'.format(request.headers.get('Authorization'), user_Id[1]))
            return make_response(jsonify({'message':'failed'})), 401
        else:
            logger.info('user {} accessing  /api/getlisttech'.format(user_Id))
            role=UserModel.query.filter_by(userId=user_Id).first()
            if(role.role == 'Admin'):
                totalT=TicketModel.query.order_by().count()
                newT=TicketModel.query.filter_by(status = 'NEW').count()
                closedT=TicketModel.query.filter_by(status = 'CLOSED').count()
                solvedT=TicketModel.query.filter_by(status = 'SOLVED').count()
                unsolvedT=TicketModel.query.filter_by(status = 'UNSOLVED').count()
                assignedT=TicketModel.query.filter_by(status = 'ASSIGNED').count()
                
                return make_response(jsonify({'totalT':totalT,'newT':newT,'closedT':closedT,'solvedT':solvedT,'unsolvedT':unsolvedT,'assignedT':assignedT}))
                
            elif(role.role == 'Technician'):
                totalT=Assign_ticketModel.query.filter_by(user_id = user_Id).count()
                newT=Assign_ticketModel.query.filter_by(user_id = user_Id, status = 'NEW').count()
                assignedT=TicketModel.query.filter_by(user_id = user_Id , status = 'ASSIGNED').count()
                closedT=TicketModel.query.join(Assign_ticketModel, TicketModel.ticketId==Assign_ticketModel.ticket_id).filter(Assign_ticketModel.user_id == user_Id, TicketModel.status=='CLOSED').count()
                solvedT=TicketModel.query.join(Assign_ticketModel, TicketModel.ticketId==Assign_ticketModel.ticket_id).filter(Assign_ticketModel.user_id == user_Id, TicketModel.status=='SOLVED').count()
                unsolvedT=TicketModel.query.join(Assign_ticketModel, TicketModel.ticketId==Assign_ticketModel.ticket_id).filter(Assign_ticketModel.user_id == user_Id, TicketModel.status=='UNSOLVED').count()
                
                return make_response(jsonify({'totalT':totalT,'newT':newT,'closedT':closedT,'solvedT':solvedT,'unsolvedT':unsolvedT,'assignedT':assignedT}))
                
            elif(role.role == 'User'):
                totalT=TicketModel.query.filter_by(user_id = user_Id).count()
                newT=TicketModel.query.filter_by(user_id = user_Id , status ='NEW').count()
                closedT=TicketModel.query.filter_by(user_id = user_Id , status = 'CLOSED').count()
                solvedT=TicketModel.query.filter_by(user_id = user_Id , status = 'SOLVED').count()
                unsolvedT=TicketModel.query.filter_by(user_id = user_Id , status = 'UNSOLVED').count()
                assignedT=TicketModel.query.filter_by(user_id = user_Id , status = 'ASSIGNED').count()
                
                return make_response(jsonify({'totalT':totalT,'newT':newT,'closedT':closedT,'solvedT':solvedT,'unsolvedT':unsolvedT,'assignedT':assignedT}))

class GetDatesAPI(MethodView):
    """get data as per the date"""
    def post(self):
        user_Id=UserModel.verify_auth_header(request.headers.get('Authorization'))
        if not isinstance(user_Id, str):
            logger.warning('user session {} -->[{}]'.format(request.headers.get('Authorization'), user_Id[1]))
            return make_response(jsonify({'message':'failed'})), 401
        else:
            logger.info('user {} accessing  /api/getstatsdate'.format(user_Id))
            role=UserModel.query.filter_by(userId=user_Id).first()
            post_data = request.get_json()
            
            if(role.role == 'Admin'):
                totalT=TicketModel.query.filter(TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                newT=TicketModel.query.filter_by(status = 'NEW').filter(TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                closedT=TicketModel.query.filter_by(status = 'CLOSED').filter(TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                solvedT=TicketModel.query.filter_by(status = 'SOLVED').filter(TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                unsolvedT=TicketModel.query.filter_by(status = 'UNSOLVED').filter(TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                assignedT=TicketModel.query.filter_by(status = 'ASSIGNED').filter(TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                
                return make_response(jsonify({'totalT':totalT,'newT':newT,'closedT':closedT,'solvedT':solvedT,'unsolvedT':unsolvedT,'assignedT':assignedT}))
                
            elif(role.role == 'Technician'):
                totalT=Assign_ticketModel.query.filter_by(user_id = user_Id).filter(Assign_ticketModel.assigned_on.between(post_data.get('start'),post_data.get('end'))).count()
                newT=Assign_ticketModel.query.filter_by(user_id = user_Id, status = 'NEW').filter(Assign_ticketModel.assigned_on.between(post_data.get('start'),post_data.get('end'))).count()
                assignedT=TicketModel.query.filter_by(user_id = user_Id , status = 'ASSIGNED').filter(TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                closedT=TicketModel.query.join(Assign_ticketModel, TicketModel.ticketId==Assign_ticketModel.ticket_id).filter(Assign_ticketModel.user_id == user_Id, TicketModel.status=='CLOSED' , TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                solvedT=TicketModel.query.join(Assign_ticketModel, TicketModel.ticketId==Assign_ticketModel.ticket_id).filter(Assign_ticketModel.user_id == user_Id, TicketModel.status=='SOLVED', TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                unsolvedT=TicketModel.query.join(Assign_ticketModel, TicketModel.ticketId==Assign_ticketModel.ticket_id).filter(Assign_ticketModel.user_id == user_Id, TicketModel.status=='UNSOLVED', TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                
                return make_response(jsonify({'totalT':totalT,'newT':newT,'closedT':closedT,'solvedT':solvedT,'unsolvedT':unsolvedT,'assignedT':assignedT}))
                
            elif(role.role == 'User'):
                totalT=TicketModel.query.filter_by(user_id = user_Id).filter(TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                newT=TicketModel.query.filter_by(user_id = user_Id , status ='NEW').filter(TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                closedT=TicketModel.query.filter_by(user_id = user_Id , status = 'CLOSED').filter(TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                solvedT=TicketModel.query.filter_by(user_id = user_Id , status = 'SOLVED').filter(TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                unsolvedT=TicketModel.query.filter_by(user_id = user_Id , status = 'UNSOLVED').filter(TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                assignedT=TicketModel.query.filter_by(user_id = user_Id , status = 'ASSIGNED').filter(TicketModel.updated_at.between(post_data.get('start'),post_data.get('end'))).count()
                
                return make_response(jsonify({'totalT':totalT,'newT':newT,'closedT':closedT,'solvedT':solvedT,'unsolvedT':unsolvedT,'assignedT':assignedT}))

            
#define the API Endpoints
getdata_view = GetDataApi.as_view('getdata_api')
getticket_view = GetTicketAPI.as_view('getticket_api')
search_view = SearchAPI.as_view('search_api')
getlisttech_view = GetListTechAPI.as_view('getlisttech_api')
stats_view = GetStatsAPI.as_view('stats_api')
getdates_view = GetDatesAPI.as_view('getdates_api')

#add Rules for API EndPoints
api_blueprint.add_url_rule(
    '/api/getdata',
    view_func=getdata_view,
    methods=['POST']
)
api_blueprint.add_url_rule(
    '/api/getticket',
    view_func= getticket_view,
    methods=['POST']
)
api_blueprint.add_url_rule(
    '/api/search',
    view_func= search_view,
    methods=['POST']
)
api_blueprint.add_url_rule(
    '/api/getlisttech',
    view_func= getlisttech_view,
    methods=['GET']
)
api_blueprint.add_url_rule(
    '/api/stats',
    view_func= stats_view,
    methods=['GET']
)
api_blueprint.add_url_rule(
    '/api/getdates',
    view_func=getdates_view,
    methods=['POST']
)