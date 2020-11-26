import os

class Config(object):
    SECRET_KEY = "LP\xb6SOI7\x16\xb0\xd9r\xb0\x1a\x9bFl>\x84\xcd\xd8\xd9\x15\x8f\x8e"
    SQLALCHEMY_DATABASE_URI= 'postgresql://kibe:denis@localhost/ticket_app'
    #SIJAX_STATIC_PATH ='app/static/js/sijax/sijax.js'
    #SIJAX_JSON_URI = 'app/static/js/sijax/json2.js'
    CSRF_ENABLED=True
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = 'app/static/uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    #SESSION_COOKIE_SECURE = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
class ProductionConfig(Config):
    DEBUG = False
    
class StagigConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True