from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, logger
from app.models import UserModel
import random, string

auth_blueprint = Blueprint('auth', __name__)

class RegisterAPI(MethodView):
    """ User Registration Resource"""
    def post(self):
        user_Id=UserModel.verify_auth_header(request.headers.get('Authorization'))
        if not isinstance(user_Id, str):
            logger.warning('user session {} -->[{}]'.format(request.headers.get('Authorization'), user_Id[1]))
            return make_response(jsonify({'message':'failed'})), 401
        else:
            logger.info('user {} allowed to register'.format(user_Id))
            #get the post data
            post_data = request.get_json()
            #check if user already exists
            user= UserModel.query.filter_by(email=post_data.get('email')).first()
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
                    logger.info('user {} succeded in registering a user'.format(user_Id))
                    return make_response(jsonify(responseObject)), 201
                except Exception as e:
                    print(e)
                    responseObject = {
                        'status' : 'fail',
                        'message': 'Some error occurred. Please try again.'
                    }
                    logger.warning('user {} experienced an error --> [{}]'.format(user_Id,responseObject['status']))
                    return make_response(jsonify(responseObject)), 202
            else:
                responseObject={
                    'status':'fail',
                    'message':'email is already taken'
                }
                logger.warning('user {} experienced error --> [{}]'.format(user_Id,responseObject['message']))
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
                        logger.info('user {} -->[{}]'.format(post_data.get('username'),responseObject['message']))
                        return make_response(jsonify(responseObject)), 200
                    else:
                        responseObject = {
                            'status':'fail',
                            'message' : 'User does not exist.'
                        }
                        logger.warning('user {} --> [{}] '.format(post_data.get('username'),responseObject['message']))
                        return make_response(jsonify(responseObject)),404
                else:
                    responseObject= {
                        'status':'fail',
                        'message':'Wrong password'
                    }
                    logger.warning('user {} --> [{}] '.format(post_data.get('username'),responseObject['message']))
                    return make_response(jsonify(responseObject)), 400
            else:
                responseObject = {
                    'status' : 'fail',
                    'message' : 'Invalid username'
                }
                logger.warning('user {} --> [{}] '.format(post_data.get('username'),responseObject['message']))
                return make_response(jsonify(responseObject)), 400
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message' : 'Try again'
            }
            logger.warning('user {} --> [{}] '.format(post_data.get('username'),responseObject['status']))
            return make_response(jsonify(responseObject)), 500
        
class UserAPI(MethodView):
    """ User Resource"""
    def get(self):
        user_Id=UserModel.verify_auth_header(request.headers.get('Authorization'))
        if isinstance(user_Id, str):
            user = UserModel.query.filter_by(userId=user_Id).first()
            responseObject = {
                'status' : 'success',
                'data':{
                    'user_id': user.userId,
                    'email' : user.email,
                    'role' : user.role,
                    'username' : user.username
                }
            }
            logger.info('user {} --> [{}] '.format(user_Id,responseObject['status']))
            return make_response(jsonify(responseObject)), 200
        else:
            logger.warning('user {} --> [{}] '.format(request.headers.get('Authorization'),user_Id[1]))
            return user_Id
        
                        
            
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

