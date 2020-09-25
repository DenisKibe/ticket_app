import os

class Config(object):
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:Q36q2Unr5yvt@104.196.98.156/postgres'
    CSRF_ENABLED=True
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = 'static/uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    
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