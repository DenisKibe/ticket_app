from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import UserModel
import random, string

auth_blueprint = Blueprint('auth', __name__)

class RegisterAPI(MethodView):
    """ User Registration Resource"""
    def post(self):
        #get the post data
        post_data = request.get_json()
        #check if user already exists
        user= UserModel.query.filter_by(username=post_data.get('username')).first()
        if not user:
            try:
                user = UserModel(
                    password = generate_password_hash(post_data.get('password')),
                    email  = post_data.get('email'),
                    role  = post_data.get('role'),
                    username  = post_data.get('username'),
                    userId   = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
                )
                
                #insert the user
                db.session.add(user)
                db.session.commit()
                
                responseObject = {
                    'status':'success',
                    'message':'Successfully registered.'
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                print(e)
                responseObject = {
                    'status' : 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 202
        else:
            responseObject={
                'status':'fail',
                'message':'username is already taken'
            }
            return make_response(jsonify(responseObject)), 400
                
 
class LoginAPI(MethodView):
    """User LoginResource"""
    def post(self):
        #get the post data
        post_data = request.get_json()
        try:
            #fetch the user data
            user = UserModel.query.filter_by(username=post_data.get('username')).first()
            if user:
                if check_password_hash(user.password,post_data.get('password')):
                    auth_token = UserModel.encode_auth_token(self,user.userId)
                    if auth_token:
                        responseObject = {
                            'user_id' : user.userId,
                            'message' : 'Successfully logged in.',
                            'access_token' : auth_token.decode()
                        }
                        return make_response(jsonify(responseObject)), 200
                    else:
                        responseObject = {
                            'status':'fail',
                            'message' : 'User does not exist.'
                        }
                        return make_response(jsonify(responseObject)),404
                else:
                    responseObject= {
                        'status':'fail',
                        'message':'Wrong password'
                    }
                    return make_response(jsonify(responseObject)), 400
            else:
                responseObject = {
                    'status' : 'fail',
                    'message' : 'Invalid username'
                }
                return make_response(jsonify(responseObject)), 400
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message' : 'Try again'
            }
            return make_response(jsonify(responseObject)), 500
        
class UserAPI(MethodView):
    """ User Resource"""
    def get(self):
        #get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject ={
                    'status':'fail',
                    'message':'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)),401
        else:
            auth_token = ''
        if auth_token:
            resp=UserModel.decode_auth_token(auth_token)
            if isinstance(resp, str):
                user = UserModel.query.filter_by(userId=resp).first()
                responseObject = {
                    'status' : 'success',
                    'data':{
                        'user_id': user.userId,
                        'email' : user.email,
                        'role' : user.role,
                        'username' : user.username
                    }
                }
                return make_response(jsonify(responseObject)), 200 
            
            return make_response(resp),401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401
                        
            
#define the API Endpoints
registration_view = RegisterAPI.as_view('register_api')
login_view= LoginAPI.as_view('login_api')
user_view = UserAPI.as_view('user_api')

#add Rules for API EndPoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/status',
    view_func = user_view,
    methods=['GET']
)

