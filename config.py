import os

class Config(object):
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI='postgres+pg5432://DenisKibe@nyuki:#Wanyugik18@nyuki.postgres.database.azure.com/ticketApp'
    CSRF_ENABLED=True
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = 'static/uploads'
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