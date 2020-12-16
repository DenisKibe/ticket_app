from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from datetime import datetime
from app import db
from app.models import TicketModel, Assign_ticketModel
import random, string

api_blueprint = Blueprint('api', __name__)


class GetDataApi(MethodView):
    """
    get data resource
    """
    def post(self):
        #get data from the user
        post_data = request.get_json()
        responseBody=[]
        if post_data.get('role') == 'Admin':
            try:
                datas=TicketModel.query.filter_by(status = post_data.get('status'))
            
                #create a dict of results
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
        #elif role == 'Technician':
        #    data=TicketModel.query.filter(Assign_ticketModel.user_id == userId , TicketModel.status==urlto).all()
         #   return render_template("dash.html", data=data, title=urlto)
       # elif session.get('user_role') == 'User':
        #    data=TicketModel.query.filter_by(user_id=userId,status=urlto).all()
         #   return render_template("dash.html", data=data, title=urlto)
        
class GetTicketAPI(MethodView):
    """get ticket based on ID """
    def post(self):
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
        post_data = request.get_json()
        responseBody=[]
        
        if post_data.get('field') == 'subject':
            
            try:
                datas= TicketModel.query.filter(TicketModel.subject.like('%'+post_data.get('vall')+'%'))
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
                datas= TicketModel.query.filter(TicketModel.comment.like('%'+post_data.get('vall')+'%'))
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
                datas= TicketModel.query.filter(TicketModel.category.like('%'+post_data.get('vall')+'%'))
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
            
            
#define the API Endpoints
getdata_view = GetDataApi.as_view('getdata_api')
getticket_view = GetTicketAPI.as_view('getticket_api')
search_view = SearchAPI.as_view('search_api')

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